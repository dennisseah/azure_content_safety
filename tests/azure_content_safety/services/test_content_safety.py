from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from azure_content_safety.models import (
    DetectedGroundednessResponseDetails,
    DetectGroundednessResponse,
    DetectProtectedMaterialCodeResponse,
    DetectProtectedMaterialCodeResponseItem,
    DetectProtectedMaterialResponse,
    DocumentAnalysis,
    ImageModerationResponse,
    ModerationResponseAnalysisItem,
    PromptShieldResponse,
    TextModerationResponse,
    UserPromptAnalysis,
)
from azure_content_safety.services.content_safety import ContentSafety, ContentSafetyEnv


@pytest.fixture
def content_safety():
    return ContentSafety(
        logger=MagicMock(),
        env=ContentSafetyEnv(
            azure_content_safety_endpoint="http://example.com",
            azure_content_safety_key="key",
            azure_content_safety_api_version="1.0",
        ),
    )


@pytest.fixture
def text_moderation_response():
    return TextModerationResponse(
        blocklistsMatch=[{"key": "value"}],
        categoriesAnalysis=[
            ModerationResponseAnalysisItem(category="category", severity=1)
        ],
    )


@pytest.fixture
def image_moderation_response():
    return ImageModerationResponse(
        categoriesAnalysis=[
            ModerationResponseAnalysisItem(category="category", severity=1)
        ],
    )


class MockResponse:
    def __init__(self, json_body: dict, status: int):
        self._json_body = json_body
        self.status = status

    async def json(self):
        return self._json_body

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


def test_get_service_url(content_safety: ContentSafety):
    # act
    url = content_safety.get_service_url("service")

    # assert
    assert url == "http://example.com/contentsafety/service?api-version=1.0"


@pytest.mark.asyncio
async def test_http_post(mocker: MockerFixture, content_safety: ContentSafety):
    # arrange
    mocker.patch("aiohttp.ClientSession.post", return_value=MockResponse({}, 200))

    # act
    result = await content_safety.http_post("fn_name", "url", {})
    assert result == {}


@pytest.mark.asyncio
async def test_http_post_err(mocker: MockerFixture, content_safety: ContentSafety):
    # arrange
    mocker.patch(
        "aiohttp.ClientSession.post", return_value=MockResponse({"status": 404}, 400)
    )

    # act
    with pytest.raises(ValueError, match="Failed to fn_name: {'status': 404}"):
        await content_safety.http_post("fn_name", "url", {})


@pytest.mark.asyncio
async def test_prompt_shield(mocker: MockerFixture, content_safety: ContentSafety):
    # arrange
    return_value = PromptShieldResponse(
        userPromptAnalysis=UserPromptAnalysis(attackDetected=True),
        documentsAnalysis=[DocumentAnalysis(attackDetected=True)],
    )
    mocker.patch(
        "azure_content_safety.services.content_safety.ContentSafety.http_post",
        return_value=return_value.model_dump(),
    )

    # act
    result = await content_safety.prompt_shield("user_prompt", ["document"])
    assert result == return_value


@pytest.mark.asyncio
async def test_detect_groundedness(
    mocker: MockerFixture, content_safety: ContentSafety
):
    # arrange
    return_value = DetectGroundednessResponse(
        ungroundedDetected=True,
        ungroundedPercentage=0.5,
        ungroundedDetails=[DetectedGroundednessResponseDetails(text="text")],
    )
    mocker.patch(
        "azure_content_safety.services.content_safety.ContentSafety.http_post",
        return_value=return_value.model_dump(),
    )

    # act
    result = await content_safety.detect_groundedness("text", ["document"])
    assert result == return_value


@pytest.mark.asyncio
async def test_detect_groundedness_qna_err(
    mocker: MockerFixture, content_safety: ContentSafety
):
    # arrange

    # act
    with pytest.raises(ValueError, match="QnA data is required when task is QnA"):
        await content_safety.detect_groundedness(
            text="text",
            groundingSources=["document"],
            task="QnA",
        )


@pytest.mark.asyncio
async def test_detect_groundedness_with_qna(
    mocker: MockerFixture, content_safety: ContentSafety
):
    # arrange
    return_value = DetectGroundednessResponse(
        ungroundedDetected=True,
        ungroundedPercentage=0.5,
        ungroundedDetails=[DetectedGroundednessResponseDetails(text="text")],
    )
    mocker.patch(
        "azure_content_safety.services.content_safety.ContentSafety.http_post",
        return_value=return_value.model_dump(),
    )

    # act
    result = await content_safety.detect_groundedness(
        text="text",
        groundingSources=["document"],
        task="QnA",
        qna=MagicMock(),
    )
    assert result == return_value


@pytest.mark.asyncio
async def test_detect_protected_materials(
    mocker: MockerFixture, content_safety: ContentSafety
):
    # arrange
    return_value = DetectProtectedMaterialResponse(
        protectedMaterialAnalysis={"key": True}
    )
    mocker.patch(
        "azure_content_safety.services.content_safety.ContentSafety.http_post",
        return_value=return_value.model_dump(),
    )

    # act
    result = await content_safety.detect_protected_materials("text")
    assert result == return_value


@pytest.mark.asyncio
async def test_detect_protected_material_for_code(
    mocker: MockerFixture, content_safety: ContentSafety
):
    # arrange
    return_value = DetectProtectedMaterialCodeResponse(
        protectedMaterialAnalysis=DetectProtectedMaterialCodeResponseItem(
            detected=True,
            codeCitations=[{"key": "value"}],
        )
    )
    mocker.patch(
        "azure_content_safety.services.content_safety.ContentSafety.http_post",
        return_value=return_value.model_dump(),
    )

    # act
    result = await content_safety.detect_protected_material_for_code("code")
    assert result == return_value


@pytest.mark.asyncio
async def test_text_moderation(
    mocker: MockerFixture,
    content_safety: ContentSafety,
    text_moderation_response: TextModerationResponse,
):
    # arrange
    patched = mocker.patch(
        "azure_content_safety.services.content_safety.ContentSafety.http_post",
        return_value=text_moderation_response.model_dump(),
    )

    # act
    result = await content_safety.text_moderation("text")
    assert result == text_moderation_response
    assert "categories" not in patched.call_args.kwargs["json"]


@pytest.mark.asyncio
async def test_text_moderation_with_categories(
    mocker: MockerFixture,
    content_safety: ContentSafety,
    text_moderation_response: TextModerationResponse,
):
    # arrange
    patched = mocker.patch(
        "azure_content_safety.services.content_safety.ContentSafety.http_post",
        return_value=text_moderation_response.model_dump(),
    )

    # act
    result = await content_safety.text_moderation(text="text", categories=["category"])
    assert result == text_moderation_response
    assert patched.call_args.kwargs["json"]["categories"] == ["category"]


@pytest.mark.asyncio
async def test_text_moderation_with_blocklist_names(
    mocker: MockerFixture,
    content_safety: ContentSafety,
    text_moderation_response: TextModerationResponse,
):
    # arrange
    patched = mocker.patch(
        "azure_content_safety.services.content_safety.ContentSafety.http_post",
        return_value=text_moderation_response.model_dump(),
    )

    # act
    result = await content_safety.text_moderation(
        text="text",
        categories=["category"],
        blocklist_names=["blocklist"],
        halt_on_blocklist_hit=False,
    )
    assert result == text_moderation_response
    assert patched.call_args.kwargs["json"]["categories"] == ["category"]
    assert patched.call_args.kwargs["json"]["blocklistNames"] == ["blocklist"]
    assert patched.call_args.kwargs["json"]["haltOnBlocklistHit"] is False


@pytest.mark.asyncio
async def test_image_moderation(
    mocker: MockerFixture,
    content_safety: ContentSafety,
    image_moderation_response: ImageModerationResponse,
):
    # arrange
    patched = mocker.patch(
        "azure_content_safety.services.content_safety.ContentSafety.http_post",
        return_value=image_moderation_response.model_dump(),
    )

    # act
    result = await content_safety.image_moderation("image_base64")
    assert result == image_moderation_response
    assert "categories" not in patched.call_args.kwargs["json"]


@pytest.mark.asyncio
async def test_image_moderation_categories(
    mocker: MockerFixture,
    content_safety: ContentSafety,
    image_moderation_response: ImageModerationResponse,
):
    # arrange
    patched = mocker.patch(
        "azure_content_safety.services.content_safety.ContentSafety.http_post",
        return_value=image_moderation_response.model_dump(),
    )

    # act
    result = await content_safety.image_moderation("image_base64", ["category"])
    assert result == image_moderation_response
    assert patched.call_args.kwargs["json"]["categories"] == ["category"]
