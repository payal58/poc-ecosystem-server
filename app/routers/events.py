from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.database import get_db
from app.models import Event
from app.schemas import EventCreate, EventUpdate, EventResponse

router = APIRouter()

@router.get("/", response_model=List[EventResponse])
async def get_events(
    category: Optional[str] = None,
    audience: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all events with optional filtering"""
    query = db.query(Event)
    
    if category:
        query = query.filter(Event.category == category)
    if audience:
        query = query.filter(Event.audience == audience)
    if search:
        query = query.filter(
            or_(
                Event.title.ilike(f"%{search}%"),
                Event.description.ilike(f"%{search}%")
            )
        )
    
    events = query.order_by(Event.start_date.desc()).all()
    return events

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a single event by ID"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """Create a new event"""
    db_event = Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing event"""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    update_data = event_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete an event"""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    db.delete(db_event)
    db.commit()
    return None

