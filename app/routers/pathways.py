from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Pathway, Organization, Event
from app.schemas import (
    PathwayCreate,
    PathwayUpdate,
    PathwayResponse,
    PathwayQuery,
    PathwayQueryResponse
)
from app.services.gemini_service import get_gemini_response

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
    """Submit pathway responses and get AI-powered recommendations from Gemini"""
    try:
        # Get all database data
        pathways = db.query(Pathway).all()
        organizations = db.query(Organization).all()
        events = db.query(Event).all()
        
        # Get Gemini AI response
        ai_response = get_gemini_response(
            user_responses=query.responses,
            pathways=pathways,
            organizations=organizations,
            events=events
        )
        
        # Format response
        recommendations = [{
            "type": "ai_recommendation",
            "content": ai_response,
            "source": "gemini_ai"
        }]
        
        return PathwayQueryResponse(recommendations=recommendations)
    except ValueError as e:
        # If Gemini API key is not set, fall back to simple matching
        pathways = db.query(Pathway).all()
        recommendations = []
        
        for pathway in pathways:
            if pathway.recommended_resources:
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )

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

