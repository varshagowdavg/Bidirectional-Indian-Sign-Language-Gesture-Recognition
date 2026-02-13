"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


# Emergency Contact Schemas
class EmergencyContactBase(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    relationship_type: Optional[str] = Field(None, max_length=50)


class EmergencyContactCreate(EmergencyContactBase):
    pass


class EmergencyContactResponse(EmergencyContactBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Audio Processing Schemas
class AudioProcessRequest(BaseModel):
    text: Optional[str] = None  # For text-to-gesture


class AudioProcessResponse(BaseModel):
    transcribed_text: str
    generated_image_url: str
    word_count: int
    processing_time: float


# Gesture Recognition Schemas
class GestureRecognitionRequest(BaseModel):
    image_data: str  # Base64 encoded image


class GestureRecognitionResponse(BaseModel):
    recognized_character: str
    confidence: float
    hand_type: str  # "one_hand" or "two_hand"
    landmarks: Optional[List[dict]] = None


class GestureSessionResponse(BaseModel):
    id: int
    recognized_text: str
    confidence_score: int
    gesture_count: int
    session_duration: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Emergency Message Schema
class EmergencyMessageRequest(BaseModel):
    message: str = Field(..., max_length=500)
    contact_ids: List[int] = Field(..., min_items=1)


class EmergencyMessageResponse(BaseModel):
    success: bool
    sent_count: int
    failed_count: int
    message: str
