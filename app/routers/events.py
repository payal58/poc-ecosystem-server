from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import date
import httpx
import requests
import cloudscraper
import asyncio
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

@router.get("/external/fetch")
async def fetch_external_events():
    """Fetch events from external API (webusinesscentre.com)"""
    try:
        # Get today's date and format for API (YYYY-MM-DD)
        today = date.today()
        today_str = today.isoformat()
        
        # Construct the API URL - fetch events from today onwards
        url = (
            f"https://www.webusinesscentre.com/wp-json/tribe/events/v1/events/"
            f"?page=1&per_page=1000&start_date={today_str}+00:00:00&status=publish"
        )
        
        # Fetch from external API - use cloudscraper to bypass Cloudflare protection
        # Run sync cloudscraper in thread pool since endpoint is async
        def fetch_with_cloudscraper():
            try:
                # Create a cloudscraper session (handles Cloudflare challenges)
                scraper = cloudscraper.create_scraper(
                    browser={
                        'browser': 'chrome',
                        'platform': 'darwin',
                        'desktop': True
                    }
                )
                response = scraper.get(url, timeout=30)
                return response
            except Exception as e:
                print(f"Cloudscraper failed: {str(e)}")
                return None
        
        # Run cloudscraper in executor
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, fetch_with_cloudscraper)
        
        if response is None or response.status_code != 200:
            # Fallback to regular requests
            def fetch_with_requests():
                try:
                    session = requests.Session()
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Referer": "https://www.webusinesscentre.com/",
                    }
                    session.headers.update(headers)
                    return session.get(url, timeout=30, allow_redirects=True)
                except Exception as e:
                    print(f"Requests fallback failed: {str(e)}")
                    return None
            
            response = await loop.run_in_executor(None, fetch_with_requests)
        
        if response is None:
            return {
                "events": [],
                "count": 0,
                "source": "webusinesscentre.com",
                "error": "API access temporarily unavailable due to security restrictions"
            }
        
        if response.status_code == 403:
            print("Warning: External API is blocking requests (403 Forbidden).")
            return {
                "events": [],
                "count": 0,
                "source": "webusinesscentre.com",
                "error": "API access temporarily unavailable due to security restrictions"
            }
        
        if response.status_code != 200:
            response.raise_for_status()
        
        data = response.json()
        
        # Transform external events to match our EventResponse schema
        external_events = []
        if "events" in data:
            for ext_event in data["events"]:
                try:
                    # Extract category names
                    categories = ext_event.get("categories", [])
                    category = ", ".join([cat.get("name", "") for cat in categories]) if categories else None
                    
                    # Extract venue information
                    venue = ext_event.get("venue", {})
                    location_parts = []
                    if venue and isinstance(venue, dict):
                        if venue.get("venue"):
                            location_parts.append(venue["venue"])
                        if venue.get("address"):
                            location_parts.append(venue["address"])
                        if venue.get("city"):
                            location_parts.append(venue["city"])
                        if venue.get("province"):
                            location_parts.append(venue["province"])
                    location = ", ".join(location_parts) if location_parts else "Location TBD"
                    
                    # Parse dates - preserve full datetime for frontend time formatting
                    start_date_str = ext_event.get("start_date", "")
                    end_date_str = ext_event.get("end_date", "")
                    
                    # Convert datetime string to ISO format for frontend
                    # External API format: "2025-11-12 16:30:00"
                    # Convert to ISO: "2025-11-12T16:30:00"
                    start_date_iso = start_date_str.replace(" ", "T") if start_date_str else f"{today}T00:00:00"
                    end_date_iso = end_date_str.replace(" ", "T") if end_date_str else None
                    
                    # Handle image safely
                    image_url = None
                    image_data = ext_event.get("image")
                    if image_data and isinstance(image_data, dict):
                        image_url = image_data.get("url")
                    
                    # Create event object matching our schema
                    transformed_event = {
                        "id": f"ext_{ext_event.get('id')}",  # Prefix to avoid conflicts
                        "title": ext_event.get("title", "Untitled Event"),
                        "description": ext_event.get("description", ""),
                        "category": category,
                        "audience": None,  # Not available in external API
                        "location": location,
                        "start_date": start_date_iso,  # Full datetime in ISO format
                        "end_date": end_date_iso,  # Full datetime in ISO format
                        "link": ext_event.get("website") or ext_event.get("url"),
                        "external": True,  # Flag to identify external events
                        "external_id": ext_event.get("id"),
                        "external_url": ext_event.get("url"),
                        "image": image_url,
                        "cost": ext_event.get("cost", ""),
                        "timezone": ext_event.get("timezone", ""),
                    }
                    external_events.append(transformed_event)
                except Exception as event_error:
                    # Log error for individual event but continue processing others
                    print(f"Error processing external event {ext_event.get('id', 'unknown')}: {str(event_error)}")
                    continue
        
        return {
            "events": external_events,
            "count": len(external_events),
            "source": "webusinesscentre.com"
        }
    except httpx.HTTPError as e:
        print(f"HTTPError fetching external events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error fetching external events: {str(e)}"
        )
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Unexpected error fetching external events: {str(e)}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )




