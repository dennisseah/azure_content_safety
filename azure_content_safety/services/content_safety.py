import logging
from dataclasses import dataclass
from typing import Any, Literal

import aiohttp
from lagom.environment import Env

from azure_content_safety.models import (
    DetectGroundednessResponse,
    DetectProtectedMaterialCodeResponse,
    DetectProtectedMaterialResponse,
    ImageModerationResponse,
    PromptShieldResponse,
    TextModerationResponse,
)
from azure_content_safety.protocols.i_content_safety import IContentSafety, QnAQuery


class ContentSafetyEnv(Env):
    azure_content_safety_endpoint: str
    azure_content_safety_key: str
    azure_content_safety_api_version: str


@dataclass
class ContentSafety(IContentSafety):
    logger: logging.Logger
    env: ContentSafetyEnv

    def get_service_url(self, service: str) -> str:
        endpoint = self.env.azure_content_safety_endpoint
        version = self.env.azure_content_safety_api_version
        return f"{endpoint}/contentsafety/{service}?api-version={version}"

    async def http_post(self, fn_name: str, url: str, json: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers={
                    "Ocp-Apim-Subscription-Key": self.env.azure_content_safety_key,
                    "Content-Type": "application/json",
                },
                json=json,
            ) as response:
                result = await response.json()
                if response.status != 200:
                    raise ValueError(f"Failed to {fn_name}: {result}")
                return result

    async def prompt_shield(
        self, user_prompt: str, documents: list[str]
    ) -> PromptShieldResponse:
        self.logger.debug("execute: prompt_shield")
        url = self.get_service_url("text:shieldPrompt")
        result = await self.http_post(
            "prompt_shield", url, {"userPrompt": user_prompt, "documents": documents}
        )
        return PromptShieldResponse(**result)

    async def detect_groundedness(
        self,
        text: str,
        groundingSources: list[str],
        reasoning: bool = False,
        domain: Literal["Medical", "Generic"] = "Generic",
        task: Literal["QnA", "Summarization"] = "Summarization",
        qna: QnAQuery | None = None,
    ) -> DetectGroundednessResponse:
        self.logger.debug("execute: detect_groundedness")
        if task == "QnA" and qna is None:
            raise ValueError("QnA data is required when task is QnA")

        input = {
            "text": text,
            "groundingSources": groundingSources,
            "reasoning": reasoning,
            "domain": domain,
            "task": task,
        }

        if task == "QnA" and qna is not None:
            input["qna"] = qna.model_dump()

        url = self.get_service_url("text:detectGroundedness")
        result = await self.http_post("detect_groundedness", url, input)
        return DetectGroundednessResponse(**result)

    async def detect_protected_materials(
        self, text: str
    ) -> DetectProtectedMaterialResponse:
        self.logger.debug("execute: detect_protected_materials")
        url = self.get_service_url("text:detectProtectedMaterial")
        result = await self.http_post("detect_protected_materials", url, {"text": text})
        return DetectProtectedMaterialResponse(**result)

    async def detect_protected_material_for_code(
        self, code: str
    ) -> DetectProtectedMaterialCodeResponse:
        self.logger.debug("execute: detect_protected_materials_for_code")
        url = self.get_service_url("text:detectProtectedMaterialForCode")
        result = await self.http_post(
            "detect_protected_material_for_code", url, {"code": code}
        )
        return DetectProtectedMaterialCodeResponse(**result)

    async def text_moderation(
        self,
        text: str,
        categories: list[str] | None = None,
        blocklist_names: list[str] | None = None,
        halt_on_blocklist_hit: bool = True,
        output_type: Literal[
            "FourSeverityLevels", "EightSeverityLevels"
        ] = "FourSeverityLevels",
    ) -> TextModerationResponse:
        self.logger.debug("execute: text_moderation")
        url = self.get_service_url("text:analyze")

        input: dict[str, str | list[str] | bool] = {
            "text": text,
            "outputType": output_type,
        }
        if categories is not None:
            input["categories"] = categories

        if blocklist_names is not None:
            input["blocklistNames"] = blocklist_names
            input["haltOnBlocklistHit"] = halt_on_blocklist_hit

        result = await self.http_post(fn_name="text_moderation", url=url, json=input)
        return TextModerationResponse(**result)

    async def image_moderation(
        self,
        image: str,
        categories: list[str] | None = None,
        output_type: Literal[
            "FourSeverityLevels", "EightSeverityLevels"
        ] = "FourSeverityLevels",
    ) -> ImageModerationResponse:
        self.logger.debug("execute: image_moderation")
        url = self.get_service_url("image:analyze")
        input: dict[str, Any] = {
            "image": {"content": image},
            "outputType": output_type,
        }
        if categories is not None:
            input["categories"] = categories

        result = await self.http_post(fn_name="image_moderation", url=url, json=input)
        return ImageModerationResponse(**result)
