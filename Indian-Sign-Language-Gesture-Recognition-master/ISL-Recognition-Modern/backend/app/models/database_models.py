"""
Database models for the ISL Recognition system.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model for authentication and profile management."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    emergency_contacts = relationship("EmergencyContact", back_populates="user", cascade="all, delete-orphan")
    audio_records = relationship("AudioRecord", back_populates="user", cascade="all, delete-orphan")


class EmergencyContact(Base):
    """Emergency contact information for users."""
    __tablename__ = "emergency_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20))
    relationship_type = Column(String(50))  # e.g., "family", "friend", "caregiver"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="emergency_contacts")


class AudioRecord(Base):
    """Record of audio-to-gesture conversions."""
    __tablename__ = "audio_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    audio_filename = Column(String(255))
    transcribed_text = Column(Text)
    generated_image_path = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="audio_records")


class GestureSession(Base):
    """Record of gesture recognition sessions."""
    __tablename__ = "gesture_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    recognized_text = Column(Text)
    confidence_score = Column(Integer)  # Average confidence percentage
    gesture_count = Column(Integer)  # Number of gestures recognized
    session_duration = Column(Integer)  # Duration in seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
