from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
from app.database import get_db
from app.models import Program, Organization
from app.schemas import (
    ProgramCreate,
    ProgramUpdate,
    ProgramResponse
)

router = APIRouter()

@router.get("/", response_model=List[ProgramResponse])
async def get_programs(
    search: Optional[str] = None,
    organization_id: Optional[int] = None,
    organization_name: Optional[str] = None,
    program_type: Optional[str] = None,
    stage: Optional[str] = None,
    sector: Optional[str] = None,
    is_active: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """Get all programs with optional filtering"""
    try:
        query = db.query(Program)
        
        # Filter by active status
        if is_active is not None:
            query = query.filter(Program.is_active == is_active)
        
        # Apply search filter
        if search:
            search_lower = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    Program.title.ilike(search_lower),
                    Program.description.ilike(search_lower)
                )
            )
        
        # Filter by organization
        if organization_id:
            query = query.filter(Program.organization_id == organization_id)
        elif organization_name:
            org = (
                db.query(Organization)
                .filter(Organization.organization_name.ilike(f"%{organization_name}%"))
                .first()
            )
            if org:
                query = query.filter(Program.organization_id == org.id)
        
        # Filter by program type
        if program_type:
            query = query.filter(Program.program_type.ilike(f"%{program_type}%"))
        
        # Filter by stage
        if stage:
            query = query.filter(Program.stage.ilike(f"%{stage}%"))
        
        # Filter by sector
        if sector:
            query = query.filter(Program.sector.ilike(f"%{sector}%"))
        
        # Order by title
        programs = query.order_by(func.coalesce(Program.title, '').asc()).all()
        
        # Convert to response format with organization name
        result = []
        for program in programs:
            org = db.query(Organization).filter(Organization.id == program.organization_id).first()
            program_dict = {
                "id": program.id,
                "title": program.title,
                "description": program.description,
                "organization_id": program.organization_id,
                "organization_name": org.organization_name if org else None,
                "program_type": program.program_type,
                "stage": program.stage,
                "sector": program.sector,
                "eligibility_criteria": program.eligibility_criteria,
                "cost": program.cost,
                "duration": program.duration,
                "application_deadline": program.application_deadline,
                "start_date": program.start_date,
                "website": program.website,
                "application_link": program.application_link,
                "is_verified": program.is_verified,
                "is_active": program.is_active,
                "created_at": program.created_at,
                "updated_at": program.updated_at,
            }
            result.append(ProgramResponse(**program_dict))
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching programs: {str(e)}"
        )

@router.get("/{program_id}", response_model=ProgramResponse)
async def get_program(program_id: int, db: Session = Depends(get_db)):
    """Get a single program by ID"""
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program with id {program_id} not found"
        )
    
    org = db.query(Organization).filter(Organization.id == program.organization_id).first()
    program_dict = {
        "id": program.id,
        "title": program.title,
        "description": program.description,
        "organization_id": program.organization_id,
        "organization_name": org.organization_name if org else None,
        "program_type": program.program_type,
        "stage": program.stage,
        "sector": program.sector,
        "eligibility_criteria": program.eligibility_criteria,
        "cost": program.cost,
        "duration": program.duration,
        "application_deadline": program.application_deadline,
        "start_date": program.start_date,
        "website": program.website,
        "application_link": program.application_link,
        "is_verified": program.is_verified,
        "is_active": program.is_active,
        "created_at": program.created_at,
        "updated_at": program.updated_at,
    }
    return ProgramResponse(**program_dict)

@router.post("/", response_model=ProgramResponse, status_code=status.HTTP_201_CREATED)
async def create_program(
    program: ProgramCreate,
    db: Session = Depends(get_db)
):
    """Create a new program"""
    # Verify organization exists
    org = db.query(Organization).filter(Organization.id == program.organization_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {program.organization_id} not found"
        )
    
    db_program = Program(**program.model_dump())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    
    program_dict = {
        "id": db_program.id,
        "title": db_program.title,
        "description": db_program.description,
        "organization_id": db_program.organization_id,
        "organization_name": org.organization_name,
        "program_type": db_program.program_type,
        "stage": db_program.stage,
        "sector": db_program.sector,
        "eligibility_criteria": db_program.eligibility_criteria,
        "cost": db_program.cost,
        "duration": db_program.duration,
        "application_deadline": db_program.application_deadline,
        "start_date": db_program.start_date,
        "website": db_program.website,
        "application_link": db_program.application_link,
        "is_verified": db_program.is_verified,
        "is_active": db_program.is_active,
        "created_at": db_program.created_at,
        "updated_at": db_program.updated_at,
    }
    return ProgramResponse(**program_dict)

@router.put("/{program_id}", response_model=ProgramResponse)
async def update_program(
    program_id: int,
    program_update: ProgramUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing program"""
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program with id {program_id} not found"
        )
    
    # Update fields
    update_data = program_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_program, field, value)
    
    db.commit()
    db.refresh(db_program)
    
    org = db.query(Organization).filter(Organization.id == db_program.organization_id).first()
    program_dict = {
        "id": db_program.id,
        "title": db_program.title,
        "description": db_program.description,
        "organization_id": db_program.organization_id,
        "organization_name": org.organization_name if org else None,
        "program_type": db_program.program_type,
        "stage": db_program.stage,
        "sector": db_program.sector,
        "eligibility_criteria": db_program.eligibility_criteria,
        "cost": db_program.cost,
        "duration": db_program.duration,
        "application_deadline": db_program.application_deadline,
        "start_date": db_program.start_date,
        "website": db_program.website,
        "application_link": db_program.application_link,
        "is_verified": db_program.is_verified,
        "is_active": db_program.is_active,
        "created_at": db_program.created_at,
        "updated_at": db_program.updated_at,
    }
    return ProgramResponse(**program_dict)

@router.delete("/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_program(program_id: int, db: Session = Depends(get_db)):
    """Delete a program"""
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program with id {program_id} not found"
        )
    
    db.delete(db_program)
    db.commit()
    return None

