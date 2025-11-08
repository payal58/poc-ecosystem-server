from pydantic import BaseModel, HttpUrl, field_validator
from datetime import date, datetime
from typing import Optional, Dict, Any, List

# Event Schemas
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    audience: Optional[str] = None
    location: str
    start_date: date
    end_date: Optional[date] = None
    link: Optional[str] = None
    
    @field_validator('link')
    @classmethod
    def validate_link(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Link must be a valid URL')
        return v

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    audience: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    link: Optional[str] = None

class EventResponse(EventBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Organization Schemas
class OrganizationBase(BaseModel):
    organization_name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    province_state: Optional[str] = None
    sector_type: Optional[str] = None
    services_offered: Optional[str] = None
    website: Optional[str] = None
    email_address: Optional[str] = None
    phone_number: Optional[str] = None
    contact_name: Optional[str] = None
    notes: Optional[str] = None
    
    @field_validator('website')
    @classmethod
    def validate_website(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Website must be a valid URL')
        return v
    
    @field_validator('email_address')
    @classmethod
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Email must be a valid email address')
        return v

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    organization_name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    province_state: Optional[str] = None
    sector_type: Optional[str] = None
    services_offered: Optional[str] = None
    website: Optional[str] = None
    email_address: Optional[str] = None
    phone_number: Optional[str] = None
    contact_name: Optional[str] = None
    notes: Optional[str] = None

class OrganizationResponse(OrganizationBase):
    id: str  # Changed to str to support external IDs like "ext_123"
    created_at: Optional[datetime] = None
    external: Optional[bool] = None  # Flag to identify external organizations
    external_id: Optional[int] = None  # Original external ID
    external_url: Optional[str] = None  # URL to external source
    
    class Config:
        from_attributes = True

# Pathway Schemas
class PathwayBase(BaseModel):
    question: str
    answer_options: Optional[Dict[str, Any]] = None
    recommended_resources: Optional[Dict[str, Any]] = None

class PathwayCreate(PathwayBase):
    pass

class PathwayUpdate(BaseModel):
    question: Optional[str] = None
    answer_options: Optional[Dict[str, Any]] = None
    recommended_resources: Optional[Dict[str, Any]] = None

class PathwayResponse(PathwayBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PathwayQuery(BaseModel):
    responses: Dict[str, Any]

class PathwayQueryResponse(BaseModel):
    recommendations: List[Dict[str, Any]]

# Search Log Schemas
class SearchLogCreate(BaseModel):
    query: str
    results_count: int = 0

class SearchLogResponse(BaseModel):
    id: int
    query: str
    results_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

