from sqlalchemy import Column, Integer, String, Text, Date, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    category = Column(String)
    audience = Column(String)
    location = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    link = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, nullable=False, index=True)  # Business Name*
    business_stage = Column(String, nullable=False)  # Business Stage*: Idea, Early Stage, Growing Business, Established Business
    description = Column(Text, nullable=False)  # Description*
    industry = Column(String, nullable=False, index=True)  # Industry*
    business_sector = Column(String)  # Business Sector (dropdown)
    business_location = Column(String, nullable=False)  # Business Location*
    legal_structure = Column(String, nullable=False)  # Legal Structure*: Sole Proprietorship, Partnership, Corporation, LLC, Non-Profit, Other
    business_status = Column(String, nullable=False)  # Business Status*: Active, Inactive, Pending, On Hold
    website = Column(String)  # Website (optional)
    email = Column(String, nullable=False)  # Email*
    phone_number = Column(String, nullable=False)  # Phone Number*
    social_media = Column(JSON)  # Social Media: LinkedIn, Twitter/X, Facebook, Instagram, YouTube, TikTok, Pinterest
    additional_contact_info = Column(Text)  # Additional Contact Info
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Pathway(Base):
    __tablename__ = "pathways"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer_options = Column(JSON)
    recommended_resources = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SearchLog(Base):
    __tablename__ = "search_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    results_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

