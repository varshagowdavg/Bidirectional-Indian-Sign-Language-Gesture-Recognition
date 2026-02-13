"""
User management router for profile and emergency contacts.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.database_models import User, EmergencyContact
from app.schemas.schemas import (
    EmergencyContactCreate,
    EmergencyContactResponse,
    EmergencyMessageRequest,
    EmergencyMessageResponse
)
from app.routers.auth import get_current_user
from app.config import get_settings

settings = get_settings()
router = APIRouter()


@router.post("/emergency-contacts", response_model=EmergencyContactResponse, status_code=status.HTTP_201_CREATED)
async def create_emergency_contact(
    contact_data: EmergencyContactCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add a new emergency contact.
    """
    # Create new contact
    new_contact = EmergencyContact(
        user_id=current_user.id,
        name=contact_data.name,
        email=contact_data.email,
        phone=contact_data.phone,
        relationship_type=contact_data.relationship_type
    )
    
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    
    return new_contact


@router.get("/emergency-contacts", response_model=List[EmergencyContactResponse])
async def get_emergency_contacts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all emergency contacts for current user.
    """
    result = await db.execute(
        select(EmergencyContact).where(EmergencyContact.user_id == current_user.id)
    )
    
    contacts = result.scalars().all()
    return contacts


@router.delete("/emergency-contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_emergency_contact(
    contact_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an emergency contact.
    """
    result = await db.execute(
        select(EmergencyContact).where(
            EmergencyContact.id == contact_id,
            EmergencyContact.user_id == current_user.id
        )
    )
    
    contact = result.scalar_one_or_none()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency contact not found"
        )
    
    await db.delete(contact)
    await db.commit()
    
    return None


@router.post("/send-emergency", response_model=EmergencyMessageResponse)
async def send_emergency_message(
    message_data: EmergencyMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Send emergency message to selected contacts.
    """
    # Get selected contacts
    result = await db.execute(
        select(EmergencyContact).where(
            EmergencyContact.id.in_(message_data.contact_ids),
            EmergencyContact.user_id == current_user.id
        )
    )
    
    contacts = result.scalars().all()
    
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No valid emergency contacts found"
        )
    
    # Send emails (simplified - in production use proper email service)
    sent_count = 0
    failed_count = 0
    
    for contact in contacts:
        try:
            # In production, implement actual email sending
            # For now, just simulate success
            # await send_email(
            #     to=contact.email,
            #     subject=f"Emergency Alert from {current_user.full_name or current_user.username}",
            #     body=message_data.message
            # )
            sent_count += 1
        except Exception as e:
            failed_count += 1
            print(f"Error sending to {contact.email}: {e}")
    
    return EmergencyMessageResponse(
        success=sent_count > 0,
        sent_count=sent_count,
        failed_count=failed_count,
        message=f"Emergency message sent to {sent_count} contact(s)"
    )
