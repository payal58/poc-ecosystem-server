from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.database import get_db
from app.models import Organization
from app.schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse
)

router = APIRouter()

@router.get("/", response_model=List[OrganizationResponse])
async def get_organizations(
    industry: Optional[str] = None,
    business_stage: Optional[str] = None,
    business_status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all organizations with optional filtering"""
    query = db.query(Organization)
    
    if industry:
        query = query.filter(Organization.industry == industry)
    if business_stage:
        query = query.filter(Organization.business_stage == business_stage)
    if business_status:
        query = query.filter(Organization.business_status == business_status)
    if search:
        query = query.filter(
            or_(
                Organization.business_name.ilike(f"%{search}%"),
                Organization.description.ilike(f"%{search}%"),
                Organization.industry.ilike(f"%{search}%")
            )
        )
    
    organizations = query.order_by(Organization.business_name).all()
    return organizations

@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(org_id: int, db: Session = Depends(get_db)):
    """Get a single organization by ID"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return org

@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db)
):
    """Create a new organization"""
    db_org = Organization(**organization.model_dump())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int,
    org_update: OrganizationUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing organization"""
    db_org = db.query(Organization).filter(Organization.id == org_id).first()
    if not db_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    update_data = org_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_org, key, value)
    
    db.commit()
    db.refresh(db_org)
    return db_org

@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(org_id: int, db: Session = Depends(get_db)):
    """Delete an organization"""
    db_org = db.query(Organization).filter(Organization.id == org_id).first()
    if not db_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    db.delete(db_org)
    db.commit()
    return None

