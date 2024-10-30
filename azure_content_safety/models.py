from pydantic import BaseModel


class UserPromptAnalysis(BaseModel):
    attackDetected: bool


class DocumentAnalysis(BaseModel):
    attackDetected: bool


class PromptShieldResponse(BaseModel):
    userPromptAnalysis: UserPromptAnalysis
    documentsAnalysis: list[DocumentAnalysis]


class DetectedGroundednessResponseDetails(BaseModel):
    text: str


class DetectGroundednessResponse(BaseModel):
    ungroundedDetected: bool
    ungroundedPercentage: float
    ungroundedDetails: list[DetectedGroundednessResponseDetails]


class DetectProtectedMaterialResponse(BaseModel):
    protectedMaterialAnalysis: dict[str, bool]


class DetectProtectedMaterialCodeResponseItem(BaseModel):
    detected: bool
    codeCitations: list[dict[str, str | list[str]]]


class DetectProtectedMaterialCodeResponse(BaseModel):
    protectedMaterialAnalysis: DetectProtectedMaterialCodeResponseItem


class ModerationResponseAnalysisItem(BaseModel):
    category: str
    severity: int


class TextModerationResponse(BaseModel):
    blocklistsMatch: list[dict[str, str]]
    categoriesAnalysis: list[ModerationResponseAnalysisItem]


class ImageModerationResponse(BaseModel):
    categoriesAnalysis: list[ModerationResponseAnalysisItem]
