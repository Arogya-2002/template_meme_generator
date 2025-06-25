from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import traceback
import urllib.parse
import uuid

from src.pipeline.template_meme_pipeline import TemplateMemePipeline
from src.exceptions import CustomException

app = FastAPI(
    title="Meme Generator API",
    description="Generates memes from facial emotion",
    version="1.0.0"
)

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Initialize the meme pipeline once
pipeline = TemplateMemePipeline()


@app.post("/generate-meme/")
async def generate_meme(image: UploadFile = File(...)):
    try:
        # Read uploaded image
        image_data = await image.read()
        pil_image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Run pipeline
        meme_artifact = pipeline.run(pil_image)

        # Reset BytesIO pointer
        meme_artifact.meme_image.seek(0)


        # Prepare filename for download
        filename = f"meme_{uuid.uuid4().hex[:8]}.png" # Windows-style
        encoded_filename = urllib.parse.quote(filename)

        # Return the image as downloadable
        return StreamingResponse(
            meme_artifact.meme_image,
            media_type="image/png",
            headers={
                "Content-Disposition": f'attachment; filename="{encoded_filename}"'
            }
        )

    except CustomException as ce:
        raise HTTPException(status_code=400, detail=str(ce))

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
