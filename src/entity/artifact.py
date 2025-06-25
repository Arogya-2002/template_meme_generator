from dataclasses import dataclass
from typing import List, Tuple, Optional
from PIL import Image


@dataclass
class ClassifyEmotionArtifact:
    emotion_id: int
    emotion_label: str
    confidence: float

@dataclass
class DetectFaceArtifact:
     boxes: List[Tuple[float, float, float, float]]

@dataclass
class EmotionProcessArtifact:
    face_index: int
    box: List[int]
    emotion_label: str
    emotion_id: Optional[int]
    confidence: float
    emoji: str
    error: Optional[str] = None
@dataclass
class MemeGeneratorArtifact:
    image_path: str
    top_text: str
    bottom_text: str
    meme_image: Image.Image
