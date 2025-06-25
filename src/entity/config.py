# from dataclasses import dataclass

# @dataclass
# class AppConfig:
#     model_name: str = "trpakov/vit-face-expression"
#     keep_all_faces: bool = True


from src.exceptions import CustomException
from src.logger import logging
from src.constants import *
import sys
from facenet_pytorch import MTCNN

class ConfigEntity:
    def __init__(self):
        self.model_name = MODEL_NAME
        self.detector = MTCNN(keep_all=True)
        self.emoji_map = EMOJI_MAP
        self.gemini_model_name = GEMINI_MODEL_NAME
        self.gemini_api_key = GEMINI_API_KEY
        self.output_dir = OUTPUT_DIR
        self.templates_dir = TEMPLATES_DIR
        self.font_path = FONT_PATH
        self.memes = MEMES


class  ClassifyEmotionConfig:
    def __init__(self,config: ConfigEntity):
        try:
            self.model_name = config.model_name

        except Exception as e:
            raise CustomException(e, sys) from e
        

class DetectFaceConfig:
    def __init__(self, config: ConfigEntity):
        try:
            self.detector = config.detector
            logging.info("Face detector initialized successfully.")
        except Exception as e:
            logging.error("Failed to initialize face detector", exc_info=True)
            raise CustomException(e, sys) from e
        

class EmotionProcessorConfig:
    def __init__(self,config: ConfigEntity):
        try:
             self.emoji_map = config.emoji_map
             self.output_dir = config.output_dir

        except Exception as e:
            logging.error("Failed to initialize EmotionProcessorConfig", exc_info=True)
            raise CustomException(e, sys) from e
        

class MemeGeneratorConfig:
    def __init__(self, config: ConfigEntity):
        try:
            self.gemini_model_name = config.gemini_model_name
            self.gemini_api_key = config.gemini_api_key
            self.output_dir = config.output_dir
            self.templates_dir = config.templates_dir
            self.font_path = config.font_path
            self.memes = config.memes
            logging.info("MemeGeneratorConfig initialized successfully.")
        except Exception as e:
            logging.error("Failed to initialize MemeGeneratorConfig", exc_info=True)
            raise CustomException(e, sys) from e