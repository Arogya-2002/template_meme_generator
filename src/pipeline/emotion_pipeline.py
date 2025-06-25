from PIL import Image
from typing import List
import sys

from src.components.detect_face import FaceDetector
from src.components.classify_emotion import EmotionClassifier
from src.entity.config import EmotionProcessorConfig, ConfigEntity
from src.entity.artifact import EmotionProcessArtifact
from src.exceptions import CustomException
from src.logger import logging


class EmotionDetectionPipeline:
    def __init__(self):
        try:
            logging.info("Initializing EmotionDetectionPipeline...")
            self.config = EmotionProcessorConfig(config=ConfigEntity())
            self.face_detector = FaceDetector()
            self.emotion_classifier = EmotionClassifier()
            logging.info("EmotionDetectionPipeline initialized successfully.")
        except Exception as e:
            logging.error("Failed to initialize EmotionDetectionPipeline", exc_info=True)
            raise CustomException(e, sys)

    def run(self, image: Image.Image) -> List[EmotionProcessArtifact]:
        try:
            logging.info("Running emotion detection pipeline...")

            # Detect faces
            detection_artifact = self.face_detector.detect_faces(image)
            boxes = detection_artifact.boxes

            if not boxes:
                logging.warning("No faces detected in the image.")
                return []

            results: List[EmotionProcessArtifact] = []

            for i, box in enumerate(boxes):
                try:
                    x1, y1, x2, y2 = [int(b) for b in box]
                    cropped_face = image.crop((x1, y1, x2, y2))
                    emotion_artifact = self.emotion_classifier.predict(cropped_face)

                    results.append(EmotionProcessArtifact(
                        face_index=i + 1,
                        box=[x1, y1, x2, y2],
                        emotion_label=emotion_artifact.emotion_label,
                        emotion_id=emotion_artifact.emotion_id,
                        confidence=round(emotion_artifact.confidence * 100, 2),
                        emoji=self.config.emoji_map.get(emotion_artifact.emotion_label.lower(), "")
                    ))

                except Exception as face_err:
                    logging.error(f"Error processing face {i+1}: {str(face_err)}", exc_info=True)
                    results.append(EmotionProcessArtifact(
                        face_index=i + 1,
                        box=[0, 0, 0, 0],
                        emotion_label="Error",
                        emotion_id=None,
                        confidence=0.0,
                        emoji="",
                        error=str(face_err)
                    ))

            logging.info(f"Emotion detection complete. Total faces processed: {len(results)}")
            return results[0].emotion_label

        except Exception as e:
            logging.error("Error running emotion detection pipeline", exc_info=True)
            raise CustomException(e, sys)


