from typing import Literal, Protocol

from pydantic import BaseModel

from azure_content_safety.models import (
    DetectGroundednessResponse,
    DetectProtectedMaterialCodeResponse,
    DetectProtectedMaterialResponse,
    ImageModerationResponse,
    PromptShieldResponse,
    TextModerationResponse,
)


class QnAQuery(BaseModel):
    query: str


class IContentSafety(Protocol):
    async def prompt_shield(
        self, user_prompt: str, documents: list[str]
    ) -> PromptShieldResponse:
        """
        In this quickstart, you use the "Prompt Shields" feature. Prompt Shields in
        Azure AI Content Safety are designed to safeguard generative AI systems from
        generating harmful or inappropriate content. These shields detect and mitigate
        risks associated with both User Prompt Attacks (malicious or harmful
        user-generated inputs) and Document Attacks (inputs containing harmful content
        embedded within documents). The use of "Prompt Shields" is crucial in
        environments where GenAI is employed, ensuring that AI outputs remain safe,
        compliant, and trustworthy.

        :param user_prompt: The user prompt to be shielded.
        :type user_prompt: str
        :param documents: The documents to be shielded.
        :type documents: list[str]
        :return: The response from the service.
        """
        ...

    async def detect_groundedness(
        self,
        text: str,
        groundingSources: list[str],
        reasoning: bool = False,
        domain: Literal["Medical", "Generic"] = "Generic",
        task: Literal["QnA", "Summarization"] = "Summarization",
        qna: QnAQuery | None = None,
    ) -> DetectGroundednessResponse:
        """
        Detects and corrects ungrounded text based on the provided source documents,
        ensuring that the generated content is aligned with factual or intended
        references.

        :param domain: The domain of the grounding task.
        :type domain: Literal["MEDICAL", "GENERIC"]
        :param task: The task to be performed.
        :type task: Literal["QnA", "Summarization"]
        :param qna: Holds QnA data when the task type is QnA.
        :type qna: QnAQuery
        :param text: the LLM output text to be checked. Character limit: 7,500.
        :type text: str
        :param groundingSources: Uses an array of grounding sources to validate
        AI-generated text. See Input requirements for limits.
        :type groundingSources: list[str]
        :param reasoning: Specifies whether to use the reasoning feature. If true,
        you need to bring your own Azure OpenAI GPT4o (0513, 0806 version) to provide
        an explanation. Be careful: using reasoning increases the processing time.
        :type reasoning: bool
        :return: The response from the service.
        """
        ...

    async def detect_protected_materials(
        self, text: str
    ) -> DetectProtectedMaterialResponse:
        """
        managing risks associated with AI-generated content (English content only).
        By detecting and preventing the display of protected material, organizations
        can ensure compliance with intellectual property laws, maintain content
        originality, and protect their reputations. Protected material refers to
        content that matches known text from copyrighted sources, such as song
        lyrics, articles, recipes, or other selected web content.

        :param text: The text to be checked for protected materials.
        :type text: str
        :return: The response from the service.
        """
        ...

    async def detect_protected_material_for_code(
        self, code: str
    ) -> DetectProtectedMaterialCodeResponse:
        """
        The Protected Material for Code feature provides a comprehensive solution for
        identifying AI outputs that match code from existing GitHub repositories.
        This feature allows code generation models to be used confidently, in a way
        that enhances transparency to end users and promotes compliance with
        organizational policies.

        :param code: This is the raw code to be checked. Other non-ascii characters
        can be included..
        :type text: str
        :return: The response from the service.
        """
        ...

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
        """
        The Text Moderation feature helps organizations manage risks associated with
        AI-generated content (English content only). By detecting and preventing the
        display of inappropriate or harmful content, organizations can ensure
        compliance with legal requirements, maintain brand reputation, and protect
        users from exposure to harmful content.
        https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/harm-categories?tabs=warning

        :param text: The text to be checked for protected materials.
        :type text: str
        :param categories: an array of category names. See the Harm categories guide
        for a list of available category names. If no categories are specified, all
        four categories are used. We use multiple categories to get scores in a single
        request.
        :type categories: list[str]
        :param blocklist_names: Text blocklist Name. Only support following characters:
        0-9 A-Z a-z - . _ ~. You could attach multiple list names here.
        :type blocklist_names: list[str]
        :param halt_on_blocklist_hit: When set to true, further analyses of harmful
        content won't be performed in cases where blocklists are hit. When set to
        false, all analyses of harmful content will be performed, whether or not
        blocklists are hit.
        :type halt_on_blocklist_hit: bool
        :param output_type: "FourSeverityLevels" or "EightSeverityLevels".
        Output severities in four or eight levels, the value can be 0,2,4,6 or
        0,1,2,3,4,5,6,7.
        :type output_type: Literal["FourSeverityLevels", "EightSeverityLevels"]
        """
        ...

    async def image_moderation(
        self,
        image: str,
        categories: list[str] | None = None,
        output_type: Literal[
            "FourSeverityLevels", "EightSeverityLevels"
        ] = "FourSeverityLevels",
    ) -> ImageModerationResponse:
        """
        The Image Moderation feature helps organizations manage risks associated with
        AI-generated content (English content only). By detecting and preventing the
        display of inappropriate or harmful content, organizations can ensure
        compliance with legal requirements, maintain brand reputation, and protect
        users from exposure to harmful content.

        :param image: The image to be checked for protected materials (base64).
        :type image: str
        :param categories: an array of category names. See the Harm categories guide
        for a list of available category names. If no categories are specified, all
        four categories are used. We use multiple categories to get scores in a single
        request.
        :type categories: list[str]
        :param output_type: "FourSeverityLevels" or "EightSeverityLevels".
        Output severities in four or eight levels, the value can be 0,2,4,6 or
        0,1,2,3,4,5,6,7.
        :type output_type: Literal["FourSeverityLevels", "EightSeverityLevels"]
        """
        ...
