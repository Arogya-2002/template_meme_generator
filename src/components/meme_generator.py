from src.exceptions import CustomException
from src.logger import logging

import os, io, sys, json, random, requests
import google.generativeai as genai

from PIL import Image, ImageDraw, ImageFont
import textwrap


from src.entity.config import ConfigEntity,MemeGeneratorConfig
from src.entity.artifact import MemeGeneratorArtifact


from io import BytesIO


class MemesGenerator:
    def __init__(self):
        try:
            logging.info("Initializing MemesGenerator...")
            self.meme_generator_config = MemeGeneratorConfig(config=ConfigEntity())

            genai.configure(api_key=self.meme_generator_config.gemini_api_key)
            self.model = genai.GenerativeModel( self.meme_generator_config.gemini_model_name)
            logging.info("MemesGenerator initialized successfully.")
        except Exception as e:
            logging.error("Error initializing MemesGenerator", exc_info=True)
            raise CustomException(e, sys)

    def generate_meme_dialogues(self, emotion):
        """Generate two dialogues for the upper and lower parts of a Tenglish meme."""
        try:
            logging.info(f"Generating meme dialogues for  emotion='{emotion}'")
            prompt = f"""
            Tenglish Comedy Writer Prompt (Refined)
            You are a hilarious Tenglish (Telugu-English) comedy writer. Create two EXTREMELY FUNNY dialogues for a meme with the emotion: {emotion}
            CRITICAL INSTRUCTIONS:

            Use natural Tenglish mixing (Telugu words in English script + English)
            Make it GENUINELY FUNNY – use relatable situations, wordplay, cultural references
            First dialogue: Setup the situation/context
            Second dialogue: Deliver the punchline/twist/reaction
            Each dialogue should be 50–80 characters for perfect readability
            Use popular Telugu expressions mixed with English slang

            EMOTION-SPECIFIC GUIDANCE WITH EXAMPLES:
            Happy: Use celebrations, achievements, good news reactions

            "Friend: Bro first salary vachesindi!"
            "Me: Arre, party ki budget separate ga undhaa?"

            Sad: Use disappointments, failures, heartbreak situations

            "Crush: I think we should be just friends..."
            "Me: Anthey, na heart ki funeral arrange cheyyandi"

            Angry: Use frustration, arguments, annoying situations

            "Mom: AC enduku? Fan tho adjust avvakunda?"
            "Me: Amma, summer heat ki responsible nenu kaadhu sun!"

            Surprise: Use unexpected twists, shocking revelations

            "Friend: Naku marriage fix aipoyindi ra!"
            "Me: Enti?! Bachelor gang lo last survivor nenu aa?"

            Sarcastic: Use witty comebacks, ironic situations

            "Boss: Work from home lo comfortable ga undochu!"
            "Me: Avunu, na laptop battery ki lifetime achievement award!"

            Neutral: Use everyday relatable situations

            "Morning coffee lekunda day start ayyindi"
            "Brain: Aiyyo, today productivity mode off cheyyandi"

            Confused: Use puzzling situations, miscommunications

            "Friend: Naaku telugu lo explain cheyyi ra"
            "Me: Bro, english lo confuse ayyav telugu lo brain hang!"

            Excited: Use anticipation, enthusiasm, hype situations

            "Weekend plans ready chesukunnava?"
            "Me: Ready kaadhu, weekend kosam countdown lo unna!"

            RETURN ONLY TWO DIALOGUES – NO EXPLANATIONS, NO FORMATTING
            """
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            lines = [line.strip() for line in text.split("\n") if line.strip()]

            if len(lines) >= 2:
                logging.info("Successfully generated two dialogues.")
                return lines[0], lines[1]
            elif len(lines) == 1:
                logging.warning("Only one dialogue received. Using fallback for second line.")
                return lines[0], "Adhi kaadhu, idhi kaadhu!"
            else:
                logging.warning("No dialogues generated. Using default fallback.")
                return "Emaindhi asalu?", "Adhi kaadhu, idhi kaadhu!"

        except Exception as e:
            logging.error("Error generating meme dialogues", exc_info=True)
            raise CustomException(e, sys)

    def _create_default_template(self, template_dir):
        """Create and return the path to a default template image."""
        try:
            default_path = os.path.join(template_dir, "default_template.jpg")
            if not os.path.exists(default_path):
                dummy_image = Image.new('RGB', (800, 800), color='white')
                dummy_image.save(default_path)
                logging.info(f"Default template created at {default_path}")
            else:
                logging.info("Using cached default template.")
            return default_path
        except Exception as e:
            logging.error("Error creating default template", exc_info=True)
            raise CustomException(e, sys)

    def add_text_to_image(self, image_path, upper_text, lower_text):
        """Add the given text to the upper and lower parts of the meme template."""
        try:
            logging.info(f"Adding text to image: {image_path}")
            img = Image.open(image_path)
            width, height = img.size
            draw = ImageDraw.Draw(img)

            try:
                upper_font_size = min(int(height * 0.06), int(1000 / max(len(upper_text) / 2, 1)))
                lower_font_size = min(int(height * 0.06), int(1000 / max(len(lower_text) / 2, 1)))
                upper_font = ImageFont.truetype(self.meme_generator_config.font_path, size=upper_font_size)
                lower_font = ImageFont.truetype(self.meme_generator_config.font_path, size=lower_font_size)
            except:
                logging.warning("Custom font not found, using default font.")
                upper_font = ImageFont.load_default()
                lower_font = ImageFont.load_default()

            char_width_est = upper_font_size * 0.6
            chars_per_line = int(width * 0.8 / char_width_est)

            upper_lines = textwrap.wrap(upper_text, width=chars_per_line)
            lower_lines = textwrap.wrap(lower_text, width=chars_per_line)

            # Upper text
            upper_section_height = height * 0.4
            total_upper_text_height = len(upper_lines) * upper_font.size * 1.2
            upper_start_y = (upper_section_height - total_upper_text_height) / 2
            y_position = upper_start_y

            for line in upper_lines:
                try:
                    bbox = draw.textbbox((0, 0), line, font=upper_font)
                    text_width = bbox[2] - bbox[0]
                except AttributeError:
                    text_width = draw.textlength(line, font=upper_font)
                position = ((width - text_width) / 2, y_position)
                outline_thickness = max(2, int(upper_font_size / 10))
                for offset_x in range(-outline_thickness, outline_thickness + 1, outline_thickness):
                    for offset_y in range(-outline_thickness, outline_thickness + 1, outline_thickness):
                        if offset_x == 0 and offset_y == 0:
                            continue
                        draw.text((position[0] + offset_x, position[1] + offset_y), line, font=upper_font, fill="black")
                draw.text(position, line, font=upper_font, fill="white")
                y_position += upper_font.size * 1.2

            # Lower text
            lower_section_top = height * 0.6
            lower_section_height = height * 0.4
            total_lower_text_height = len(lower_lines) * lower_font.size * 1.2
            lower_start_y = lower_section_top + (lower_section_height - total_lower_text_height) / 2
            y_position = lower_start_y

            for line in lower_lines:
                try:
                    bbox = draw.textbbox((0, 0), line, font=lower_font)
                    text_width = bbox[2] - bbox[0]
                except AttributeError:
                    text_width = draw.textlength(line, font=lower_font)
                position = ((width - text_width) / 2, y_position)
                outline_thickness = max(2, int(lower_font_size / 10))
                for offset_x in range(-outline_thickness, outline_thickness + 1, outline_thickness):
                    for offset_y in range(-outline_thickness, outline_thickness + 1, outline_thickness):
                        if offset_x == 0 and offset_y == 0:
                            continue
                        draw.text((position[0] + offset_x, position[1] + offset_y), line, font=lower_font, fill="black")
                draw.text(position, line, font=lower_font, fill="white")
                y_position += lower_font.size * 1.2

            img_byte_array = io.BytesIO()
            img.save(img_byte_array, format='PNG')
            img_byte_array.seek(0)
            logging.info("Meme image with text generated successfully.")
            return img_byte_array

        except Exception as e:
            logging.error("Error adding text to image", exc_info=True)
            error_img = Image.new('RGB', (400, 200), color='red')
            draw = ImageDraw.Draw(error_img)
            draw.text((10, 10), f"Error: {str(e)}", fill="white")
            error_buffer = io.BytesIO()
            error_img.save(error_buffer, format='PNG')
            error_buffer.seek(0)
            return error_buffer
        


    def initiate_meme_generator(self, image_path, emotion) -> MemeGeneratorArtifact:
        try:
            os.makedirs(self.meme_generator_config.output_dir, exist_ok=True)

            # Generate meme dialogues
            upper_text, lower_text = self.generate_meme_dialogues(emotion)



            # Add text to the image and get output as BytesIO
            output_bytes = self.add_text_to_image(image_path, upper_text, lower_text)  # This should already return BytesIO
            
            logging.info("Meme generated in-memory successfully.")
            
            return  MemeGeneratorArtifact(image_path=image_path,
                                            top_text=upper_text,
                                            bottom_text=lower_text,
                                            meme_image=output_bytes)  
        except Exception as e:
           raise CustomException(e, sys)





