from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Optional
import httpx
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
    search: Optional[str] = None,
    city: Optional[str] = None,
    sector_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all organizations from database - matches new Organization model"""
    try:
        # Query organizations from database
        query = db.query(Organization)
        
        # Apply filters
        if search:
            search_lower = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    Organization.organization_name.ilike(search_lower),
                    Organization.address.ilike(search_lower),
                    Organization.city.ilike(search_lower),
                    Organization.services_offered.ilike(search_lower)
                )
            )
        
        # Filter by city
        if city:
            city_lower = city.lower().strip()
            # Handle "Windsor, ON" or "Windsor" - extract just the city name
            if city_lower == "windsor, on" or city_lower == "windsor":
                # Filter by city name "Windsor" (case-insensitive)
                query = query.filter(Organization.city.ilike("%windsor%"))
            else:
                # For other cities, do a simple match on city name
                query = query.filter(Organization.city.ilike(f"%{city_lower}%"))
        
        if sector_type:
            query = query.filter(Organization.sector_type.ilike(f"%{sector_type}%"))
        
        # Get all organizations - order by organization_name
        # Use coalesce to handle NULL values
        db_organizations = query.order_by(
            func.coalesce(Organization.organization_name, '').asc()
        ).all()
        
        # Convert to response format
        organizations = []
        for db_org in db_organizations:
            try:
                # Safely convert latitude/longitude
                lat = None
                lon = None
                if db_org.latitude is not None:
                    try:
                        lat = float(db_org.latitude)
                    except (ValueError, TypeError):
                        lat = None
                if db_org.longitude is not None:
                    try:
                        lon = float(db_org.longitude)
                    except (ValueError, TypeError):
                        lon = None
                
                org = OrganizationResponse(
                    id=str(db_org.id),  # Convert to string
                    organization_name=db_org.organization_name,
                    city=db_org.city,
                    address=db_org.address,
                    latitude=lat,
                    longitude=lon,
                    province_state=db_org.province_state,
                    sector_type=db_org.sector_type,
                    services_offered=db_org.services_offered,
                    website=db_org.website,
                    email_address=db_org.email_address,
                    phone_number=db_org.phone_number,
                    contact_name=db_org.contact_name,
                    notes=db_org.notes,
                    created_at=db_org.created_at,
                    external=False,  # Database organizations are not external
                    external_id=None,
                    external_url=None,
                )
                organizations.append(org)
            except Exception as org_error:
                print(f"Error processing organization {db_org.id}: {str(org_error)}")
                continue
        
        return organizations
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Unexpected error fetching organizations: {str(e)}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(org_id: str, db: Session = Depends(get_db)):
    """Get a single organization by ID from database"""
    try:
        # Get organization from database
        db_org = db.query(Organization).filter(Organization.id == int(org_id)).first()
        if not db_org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Convert database org to response format
        org = OrganizationResponse(
            id=str(db_org.id),  # Convert to string
            organization_name=db_org.organization_name,
            city=db_org.city,
            address=db_org.address,
            latitude=float(db_org.latitude) if db_org.latitude else None,
            longitude=float(db_org.longitude) if db_org.longitude else None,
            province_state=db_org.province_state,
            sector_type=db_org.sector_type,
            services_offered=db_org.services_offered,
            website=db_org.website,
            email_address=db_org.email_address,
            phone_number=db_org.phone_number,
            contact_name=db_org.contact_name,
            notes=db_org.notes,
            created_at=db_org.created_at,
            external=False,  # Database organizations are not external
            external_id=None,
            external_url=None,
        )
        return org
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching organization: {str(e)}"
        )

@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db)
):
    """Create a new organization in database"""
    db_org = Organization(**organization.model_dump())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    
    # Convert to response format with string ID
    org = OrganizationResponse(
        id=str(db_org.id),
        organization_name=db_org.organization_name,
        city=db_org.city,
        address=db_org.address,
        latitude=float(db_org.latitude) if db_org.latitude else None,
        longitude=float(db_org.longitude) if db_org.longitude else None,
        province_state=db_org.province_state,
        sector_type=db_org.sector_type,
        services_offered=db_org.services_offered,
        website=db_org.website,
        email_address=db_org.email_address,
        phone_number=db_org.phone_number,
        contact_name=db_org.contact_name,
        notes=db_org.notes,
        created_at=db_org.created_at,
        external=False,
        external_id=None,
        external_url=None,
    )
    return org

@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: str,
    org_update: OrganizationUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing organization in database"""
    try:
        db_org = db.query(Organization).filter(Organization.id == int(org_id)).first()
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
        
        # Convert to response format with string ID
        org = OrganizationResponse(
            id=str(db_org.id),
            organization_name=db_org.organization_name,
            city=db_org.city,
            address=db_org.address,
            latitude=float(db_org.latitude) if db_org.latitude else None,
            longitude=float(db_org.longitude) if db_org.longitude else None,
            province_state=db_org.province_state,
            sector_type=db_org.sector_type,
            services_offered=db_org.services_offered,
            website=db_org.website,
            email_address=db_org.email_address,
            phone_number=db_org.phone_number,
            contact_name=db_org.contact_name,
            notes=db_org.notes,
            created_at=db_org.created_at,
            external=False,
            external_id=None,
            external_url=None,
        )
        return org
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(org_id: str, db: Session = Depends(get_db)):
    """Delete an organization from database"""
    try:
        db_org = db.query(Organization).filter(Organization.id == int(org_id)).first()
        if not db_org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        db.delete(db_org)
        db.commit()
        return None
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

