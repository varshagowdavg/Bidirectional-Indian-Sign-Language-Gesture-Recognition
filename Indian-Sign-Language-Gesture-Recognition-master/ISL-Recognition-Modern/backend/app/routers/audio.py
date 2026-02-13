"""
Audio processing router for speech-to-gesture conversion.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, status
import aiofiles
import os
from pathlib import Path
import time
import uuid

from app.schemas.schemas import AudioProcessRequest, AudioProcessResponse
from app.services.audio_processor import get_audio_processor
from app.services.image_generator import get_image_generator
from app.config import get_settings

settings = get_settings()
router = APIRouter()

# Create upload directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
AUDIO_DIR = UPLOAD_DIR / "audio"
AUDIO_DIR.mkdir(exist_ok=True)
IMAGE_DIR = UPLOAD_DIR / "images"
IMAGE_DIR.mkdir(exist_ok=True)


@router.post("/upload", response_model=AudioProcessResponse)
async def upload_audio(
    file: UploadFile = File(...)
):
    """
    Upload audio file and convert to ISL gestures.
    """
    start_time = time.time()
    
    # Validate file format
    file_ext = file.filename.split('.')[-1].lower()
    if file_ext not in settings.allowed_audio_formats_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format. Allowed formats: {settings.allowed_audio_formats}"
        )
    
    # Generate unique filename
    unique_id = str(uuid.uuid4())
    audio_filename = f"{unique_id}.{file_ext}"
    audio_path = AUDIO_DIR / audio_filename
    
    # Save uploaded file
    try:
        async with aiofiles.open(audio_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )
    
    # Transcribe audio
    audio_processor = get_audio_processor()
    success, transcribed_text, error = audio_processor.transcribe_audio(str(audio_path))
    
    if not success:
        # Clean up file
        os.remove(audio_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error transcribing audio: {error}"
        )
    
    # Generate ISL gesture image
    image_generator = get_image_generator()
    image_filename = f"{unique_id}.png"
    image_path = IMAGE_DIR / image_filename
    
    try:
        gesture_image = image_generator.generate_sentence_image(
            transcribed_text,
            output_path=str(image_path)
        )
    except Exception as e:
        # Clean up files
        os.remove(audio_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating gesture image: {str(e)}"
        )
    
    processing_time = time.time() - start_time
    word_count = len(transcribed_text.split())
    
    return AudioProcessResponse(
        transcribed_text=transcribed_text,
        generated_image_url=f"/api/audio/images/{image_filename}",
        word_count=word_count,
        processing_time=processing_time
    )


@router.post("/text-to-gesture", response_model=AudioProcessResponse)
async def text_to_gesture(
    request: AudioProcessRequest
):
    """
    Convert text directly to ISL gesture images.
    """
    start_time = time.time()
    
    if not request.text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text is required"
        )
    
    # Generate ISL gesture image
    image_generator = get_image_generator()
    unique_id = str(uuid.uuid4())
    image_filename = f"{unique_id}.png"
    image_path = IMAGE_DIR / image_filename
    
    try:
        gesture_image = image_generator.generate_sentence_image(
            request.text,
            output_path=str(image_path)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating gesture image: {str(e)}"
        )
    
    processing_time = time.time() - start_time
    word_count = len(request.text.split())
    
    return AudioProcessResponse(
        transcribed_text=request.text,
        generated_image_url=f"/api/audio/images/{image_filename}",
        word_count=word_count,
        processing_time=processing_time
    )


@router.get("/images/{filename}")
async def get_image(filename: str):
    """
    Get generated gesture image.
    """
    from fastapi.responses import FileResponse
    
    image_path = IMAGE_DIR / filename
    
    if not image_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    return FileResponse(image_path)
