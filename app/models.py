from sqlalchemy import Column, Integer, String, Text, Date, DateTime, JSON, Numeric, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
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
    organization_name = Column(Text, index=True)
    city = Column(String(100))
    address = Column(Text)
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    province_state = Column(String(50))
    sector_type = Column(String(200))
    services_offered = Column(Text)
    website = Column(Text)
    email_address = Column(Text)
    phone_number = Column(String(50))
    contact_name = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

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

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="user", nullable=False)  # "user" or "admin"
    is_active = Column(String, default="true", nullable=False)  # Using string for compatibility
    # Extended profile fields
    business_stage = Column(String, nullable=True)  # idea, startup, growth, scale
    sector = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    profile_image = Column(String, nullable=True)
    language_preference = Column(String, default="en", nullable=False)  # en, fr, ar, zh
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    saved_programs = relationship("SavedProgram", back_populates="user", cascade="all, delete-orphan")
    saved_grants = relationship("SavedGrant", back_populates="user", cascade="all, delete-orphan")
    mentor_bookings = relationship("MentorBooking", back_populates="user", cascade="all, delete-orphan")
    user_programs = relationship("UserProgram", back_populates="user", cascade="all, delete-orphan")

class Program(Base):
    __tablename__ = "programs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    program_type = Column(String, nullable=False)  # accelerator, incubator, workshop, mentorship, etc.
    stage = Column(String, nullable=True)  # idea, startup, growth, scale
    sector = Column(String, nullable=True)  # tech, healthcare, social enterprise, etc.
    eligibility_criteria = Column(JSON, nullable=True)  # pre-revenue, student, women-led, etc.
    cost = Column(String, nullable=True)  # free, paid, sliding scale
    duration = Column(String, nullable=True)
    application_deadline = Column(Date, nullable=True)
    start_date = Column(Date, nullable=True)
    website = Column(Text, nullable=True)
    application_link = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)  # Innovation Zone Verified tag
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    organization = relationship("Organization", backref="programs")

class Mentor(Base):
    __tablename__ = "mentors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # If mentor is also a user
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    full_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    expertise_tags = Column(JSON, nullable=True)  # ["marketing", "social enterprise", "women founders"]
    sector_focus = Column(String, nullable=True)
    stage_focus = Column(String, nullable=True)  # idea, startup, growth, scale
    profile_image = Column(String, nullable=True)
    office_hours = Column(JSON, nullable=True)  # Available time slots
    is_approved = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    organization = relationship("Organization", backref="mentors")
    bookings = relationship("MentorBooking", back_populates="mentor", cascade="all, delete-orphan")

class Grant(Base):
    __tablename__ = "grants"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    grant_type = Column(String, nullable=False)  # local, provincial, federal, competition
    amount_min = Column(Numeric(12, 2), nullable=True)
    amount_max = Column(Numeric(12, 2), nullable=True)
    eligibility_criteria = Column(JSON, nullable=True)  # pre-revenue, student, women-led, BIPOC, etc.
    sector = Column(String, nullable=True)
    application_deadline = Column(Date, nullable=True, index=True)
    application_link = Column(Text, nullable=True)
    requirements = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    organization = relationship("Organization", backref="grants")

class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    resource_type = Column(String, nullable=False)  # module, template, video, article, checklist
    category = Column(String, nullable=True)  # Idea Validation, Incorporation, Finance, Pitching
    file_url = Column(Text, nullable=True)  # For downloadable files
    video_url = Column(Text, nullable=True)  # For video content
    external_link = Column(Text, nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    is_featured = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    organization = relationship("Organization", backref="resources")

class SavedProgram(Base):
    __tablename__ = "saved_programs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    reminder_date = Column(Date, nullable=True)  # For deadline reminders
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="saved_programs")
    program = relationship("Program")

class SavedGrant(Base):
    __tablename__ = "saved_grants"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    grant_id = Column(Integer, ForeignKey("grants.id"), nullable=False)
    application_status = Column(String, nullable=True)  # interested, applied, awarded, rejected
    reminder_date = Column(Date, nullable=True)  # For deadline reminders
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="saved_grants")
    grant = relationship("Grant")

class MentorBooking(Base):
    __tablename__ = "mentor_bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mentor_id = Column(Integer, ForeignKey("mentors.id"), nullable=False)
    booking_date = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, default=30, nullable=False)
    status = Column(String, default="pending", nullable=False)  # pending, confirmed, completed, cancelled
    meeting_link = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="mentor_bookings")
    mentor = relationship("Mentor", back_populates="bookings")

class UserProgram(Base):
    __tablename__ = "user_programs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    enrollment_status = Column(String, default="enrolled", nullable=False)  # enrolled, completed, dropped
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now())
    completion_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="user_programs")
    program = relationship("Program")

class Referral(Base):
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    referring_org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    receiving_org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # The entrepreneur being referred
    referral_type = Column(String, nullable=False)  # program, mentor, grant, service
    related_id = Column(Integer, nullable=True)  # ID of the program/mentor/grant being referred
    status = Column(String, default="pending", nullable=False)  # pending, accepted, completed, rejected
    notes = Column(Text, nullable=True)
    shared_notes = Column(Text, nullable=True)  # Notes visible to both orgs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    referring_org = relationship("Organization", foreign_keys=[referring_org_id], backref="referrals_sent")
    receiving_org = relationship("Organization", foreign_keys=[receiving_org_id], backref="referrals_received")
    user = relationship("User")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Admin/partner who responds
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)  # Which org should handle
    message = Column(Text, nullable=False)
    is_from_user = Column(Boolean, default=True, nullable=False)
    is_bot_response = Column(Boolean, default=False, nullable=False)
    status = Column(String, default="unanswered", nullable=False)  # unanswered, answered, resolved
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", foreign_keys=[user_id])
    admin = relationship("User", foreign_keys=[admin_id])
    organization = relationship("Organization")

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_type = Column(String, nullable=False)  # badge, milestone, engagement
    achievement_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="achievements")

