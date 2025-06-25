from src.exceptions import CustomException
from src.logger import logging
from src.components.meme_generator import MemesGenerator
from src.pipeline.emotion_pipeline import EmotionDetectionPipeline
import sys
from PIL import Image
import tempfile

class TemplateMemePipeline:
    def __init__(self):
        try:
            logging.info("Initializing TemplateMemePipeline...")
            self.emotion_pipeline = EmotionDetectionPipeline()
            self.meme_generator = MemesGenerator()

            logging.info("TemplateMemePipeline initialized successfully.")
        except Exception as e:
            logging.error("Failed to initialize TemplateMemePipeline", exc_info=True)
            raise CustomException(e, sys) from e
        
    def run(self, image: Image.Image):
        try:
            logging.info("Running TemplateMemePipeline...")

            # Step 1: Detect emotion (returns a list of EmotionProcessArtifact)
            emotion =  self.emotion_pipeline.run(image)
            logging.info(f"Emotion detection result: {emotion}")

            if not emotion:
                raise CustomException("No faces/emotions detected in the image", sys)

            # ✅ Pick the first face's emotion
         
            primary_emotion = emotion
            logging.info(f"Detected primary emotion: {primary_emotion}")

            # Step 2: Save PIL image to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                image.save(tmp.name)
                temp_image_path = tmp.name
                logging.info(f"Temporary image saved at: {temp_image_path}")

            # Step 3: Generate meme using image path and emotion
            meme_artifact = self.meme_generator.initiate_meme_generator(temp_image_path,primary_emotion)

            logging.info("TemplateMemePipeline completed successfully.")
            return meme_artifact

        except Exception as e:
            logging.error("Error running TemplateMemePipeline", exc_info=True)
            raise CustomException(e, sys)


