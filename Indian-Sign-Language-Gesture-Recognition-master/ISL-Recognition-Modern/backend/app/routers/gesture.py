"""
Gesture recognition router for real-time hand gesture processing.
"""
from fastapi import APIRouter, HTTPException, status
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

from app.schemas.schemas import GestureRecognitionRequest, GestureRecognitionResponse
from app.services.hand_tracker import HandTracker
from app.services.gesture_classifier import GestureClassifier, SpellCorrector

router = APIRouter()

# Initialize services
hand_tracker = HandTracker()
gesture_classifier = GestureClassifier()
spell_corrector = SpellCorrector()


@router.post("/recognize", response_model=GestureRecognitionResponse)
async def recognize_gesture(
    request: GestureRecognitionRequest
):
    """
    Recognize gesture from image data.
    """
    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image_data.split(',')[1] if ',' in request.image_data else request.image_data)
        image = Image.open(BytesIO(image_data))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Process frame with hand tracker
        print(f"Processing frame with shape: {frame.shape}")
        annotated_frame, hand_landmarks_list = hand_tracker.process_frame(frame)
        
        # Check if hand detection returned None or empty list
        if hand_landmarks_list is None or len(hand_landmarks_list) == 0:
            print("No hands detected in the image")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No hand detected in image"
            )
        
        print(f"Detected {len(hand_landmarks_list)} hands")
        
        # Use first detected hand
        hand_data = hand_landmarks_list[0]
        landmarks = hand_data['landmarks']
        print(f"Got {len(landmarks)} landmarks")
        
        # Classify hand type
        hand_type = hand_tracker.classify_hand_type(landmarks)
        print(f"Hand type: {hand_type}")
        
        # Extract hand region
        hand_region = hand_tracker.extract_hand_region(frame, landmarks)
        
        if hand_region is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract hand region"
            )
        
        # Preprocess for classification
        preprocessed = hand_tracker.preprocess_for_classification(hand_region)
        
        # Classify gesture
        # Use landmark-based classification with the new model
        print(f"Classifying gesture with {len(landmarks)} landmarks")
        predicted_char, confidence = gesture_classifier.classify_from_landmarks(
            landmarks,
            frame.shape[:2]
        )
        print(f"Prediction result: {predicted_char} ({confidence}%)")
        
        return GestureRecognitionResponse(
            recognized_character=predicted_char,
            confidence=confidence,
            hand_type=hand_type,
            landmarks=[{"x": lm['x'], "y": lm['y'], "z": lm['z']} for lm in landmarks]
        )
        
    except HTTPException as he:
        # Re-raise HTTP exceptions (like 400 Bad Request)
        raise he
    except Exception as e:
        import traceback
        error_detail = f"Error processing gesture: {str(e)}\n{traceback.format_exc()}"
        print(error_detail) # Print to console for immediate visibility
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing gesture: {str(e)}"
        )


@router.post("/recognize-batch")
async def recognize_gesture_batch(
    images: list[GestureRecognitionRequest]
):
    """
    Recognize multiple gestures and form words.
    """
    recognized_chars = []
    total_confidence = 0
    
    for img_request in images:
        try:
            # Process each image
            result = await recognize_gesture(img_request)
            recognized_chars.append(result.recognized_character)
            total_confidence += result.confidence
        except:
            continue
    
    if not recognized_chars:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No gestures recognized"
        )
    
    # Form word from characters
    raw_word = ''.join(recognized_chars)
    
    # Apply spell correction
    corrected_word = spell_corrector.correct_word(raw_word)
    
    avg_confidence = total_confidence / len(recognized_chars)
    
    return {
        "raw_text": raw_word,
        "corrected_text": corrected_word,
        "confidence": avg_confidence,
        "character_count": len(recognized_chars)
    }
