from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Pathway
from app.schemas import (
    PathwayCreate,
    PathwayUpdate,
    PathwayResponse,
    PathwayQuery,
    PathwayQueryResponse
)

router = APIRouter()

@router.get("/", response_model=List[PathwayResponse])
async def get_pathways(db: Session = Depends(get_db)):
    """Get all pathway questions"""
    pathways = db.query(Pathway).order_by(Pathway.id).all()
    return pathways

@router.get("/{pathway_id}", response_model=PathwayResponse)
async def get_pathway(pathway_id: int, db: Session = Depends(get_db)):
    """Get a single pathway by ID"""
    pathway = db.query(Pathway).filter(Pathway.id == pathway_id).first()
    if not pathway:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pathway not found"
        )
    return pathway

@router.post("/", response_model=PathwayResponse, status_code=status.HTTP_201_CREATED)
async def create_pathway(pathway: PathwayCreate, db: Session = Depends(get_db)):
    """Create a new pathway"""
    db_pathway = Pathway(**pathway.model_dump())
    db.add(db_pathway)
    db.commit()
    db.refresh(db_pathway)
    return db_pathway

@router.post("/query", response_model=PathwayQueryResponse)
async def query_pathway(
    query: PathwayQuery,
    db: Session = Depends(get_db)
):
    """Submit pathway responses and get recommendations"""
    # Get all pathways
    pathways = db.query(Pathway).all()
    
    # Simple matching logic: find pathways that match the responses
    recommendations = []
    
    for pathway in pathways:
        if pathway.recommended_resources:
            # Check if any response matches the pathway
            matches = False
            if pathway.answer_options:
                for key, value in query.responses.items():
                    if key in pathway.answer_options:
                        if str(value) == str(pathway.answer_options[key]):
                            matches = True
                            break
            
            if matches or not pathway.answer_options:
                recommendations.append({
                    "pathway_id": pathway.id,
                    "question": pathway.question,
                    "resources": pathway.recommended_resources
                })
    
    return PathwayQueryResponse(recommendations=recommendations)

@router.put("/{pathway_id}", response_model=PathwayResponse)
async def update_pathway(
    pathway_id: int,
    pathway_update: PathwayUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing pathway"""
    db_pathway = db.query(Pathway).filter(Pathway.id == pathway_id).first()
    if not db_pathway:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pathway not found"
        )
    
    update_data = pathway_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_pathway, key, value)
    
    db.commit()
    db.refresh(db_pathway)
    return db_pathway

@router.delete("/{pathway_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pathway(pathway_id: int, db: Session = Depends(get_db)):
    """Delete a pathway"""
    db_pathway = db.query(Pathway).filter(Pathway.id == pathway_id).first()
    if not db_pathway:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pathway not found"
        )
    db.delete(db_pathway)
    db.commit()
    return None

