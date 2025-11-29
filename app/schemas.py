from pydantic import BaseModel, HttpUrl, field_validator, EmailStr
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

# User/Auth Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    business_stage: Optional[str] = None
    sector: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    language_preference: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Program Schemas
class ProgramBase(BaseModel):
    title: str
    description: str
    organization_id: int
    program_type: str  # accelerator, incubator, workshop, mentorship, etc.
    stage: Optional[str] = None  # idea, startup, growth, scale
    sector: Optional[str] = None  # tech, healthcare, social enterprise, etc.
    eligibility_criteria: Optional[Dict[str, Any]] = None  # pre-revenue, student, women-led, etc.
    cost: Optional[str] = None  # free, paid, sliding scale
    duration: Optional[str] = None
    application_deadline: Optional[date] = None
    start_date: Optional[date] = None
    website: Optional[str] = None
    application_link: Optional[str] = None
    is_verified: Optional[bool] = False
    is_active: Optional[bool] = True

class ProgramCreate(ProgramBase):
    pass

class ProgramUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    organization_id: Optional[int] = None
    program_type: Optional[str] = None
    stage: Optional[str] = None
    sector: Optional[str] = None
    eligibility_criteria: Optional[Dict[str, Any]] = None
    cost: Optional[str] = None
    duration: Optional[str] = None
    application_deadline: Optional[date] = None
    start_date: Optional[date] = None
    website: Optional[str] = None
    application_link: Optional[str] = None
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None

class ProgramResponse(ProgramBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    organization_name: Optional[str] = None  # Include organization name for convenience
    
    class Config:
        from_attributes = True

