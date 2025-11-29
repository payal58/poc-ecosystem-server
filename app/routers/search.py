from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SearchLog
from app.schemas import SearchLogCreate, SearchLogResponse

router = APIRouter()

@router.post("/log", response_model=SearchLogResponse, status_code=status.HTTP_201_CREATED)
async def log_search(search_log: SearchLogCreate, db: Session = Depends(get_db)):
    """Log a failed or successful search query"""
    db_log = SearchLog(**search_log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/logs", response_model=List[SearchLogResponse])
async def get_search_logs(db: Session = Depends(get_db)):
    """Get all search logs (admin view)"""
    logs = db.query(SearchLog).order_by(SearchLog.created_at.desc()).all()
    return logs





