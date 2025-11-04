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
    business_name: str  # Business Name*
    business_stage: str  # Business Stage*: Idea, Early Stage, Growing Business, Established Business
    description: str  # Description*
    industry: str  # Industry*
    business_sector: Optional[str] = None  # Business Sector
    business_location: str  # Business Location*
    legal_structure: str  # Legal Structure*: Sole Proprietorship, Partnership, Corporation, LLC, Non-Profit, Other
    business_status: str  # Business Status*: Active, Inactive, Pending, On Hold
    website: Optional[str] = None  # Website
    email: str  # Email*
    phone_number: str  # Phone Number*
    social_media: Optional[Dict[str, Any]] = None  # Social Media: LinkedIn, Twitter/X, Facebook, Instagram, YouTube, TikTok, Pinterest
    additional_contact_info: Optional[str] = None  # Additional Contact Info
    
    @field_validator('website')
    @classmethod
    def validate_website(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Website must be a valid URL')
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Email must be a valid email address')
        return v
    
    @field_validator('business_stage')
    @classmethod
    def validate_business_stage(cls, v):
        allowed = ['Idea', 'Early Stage', 'Growing Business', 'Established Business']
        if v not in allowed:
            raise ValueError(f'Business stage must be one of: {", ".join(allowed)}')
        return v
    
    @field_validator('legal_structure')
    @classmethod
    def validate_legal_structure(cls, v):
        allowed = ['Sole Proprietorship', 'Partnership', 'Corporation', 'LLC', 'Non-Profit', 'Other']
        if v not in allowed:
            raise ValueError(f'Legal structure must be one of: {", ".join(allowed)}')
        return v
    
    @field_validator('business_status')
    @classmethod
    def validate_business_status(cls, v):
        allowed = ['Active', 'Inactive', 'Pending', 'On Hold']
        if v not in allowed:
            raise ValueError(f'Business status must be one of: {", ".join(allowed)}')
        return v

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    business_name: Optional[str] = None
    business_stage: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    business_sector: Optional[str] = None
    business_location: Optional[str] = None
    legal_structure: Optional[str] = None
    business_status: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    social_media: Optional[Dict[str, Any]] = None
    additional_contact_info: Optional[str] = None

class OrganizationResponse(OrganizationBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
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

