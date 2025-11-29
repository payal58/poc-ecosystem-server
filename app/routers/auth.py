from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, Token, UserLogin
from app.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password length
    if len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long"
        )
    
    # Warn if password is too long (bcrypt limit is 72 bytes)
    if len(user_data.password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too long (maximum 72 bytes). Please use a shorter password."
        )
    
    # Create new user (default role is "user" unless explicitly set to "admin")
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role or "user",
        is_active="true"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Convert is_active string to boolean for response
    user_dict = {
        "id": db_user.id,
        "email": db_user.email,
        "full_name": db_user.full_name,
        "role": db_user.role,
        "is_active": db_user.is_active == "true" if isinstance(db_user.is_active, str) else bool(db_user.is_active),
        "business_stage": db_user.business_stage,
        "sector": db_user.sector,
        "bio": db_user.bio,
        "profile_image": db_user.profile_image,
        "language_preference": db_user.language_preference,
        "created_at": db_user.created_at,
    }
    
    return UserResponse(**user_dict)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    
    # Convert is_active string to boolean for response
    user_dict = {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active == "true" if isinstance(user.is_active, str) else bool(user.is_active),
        "business_stage": user.business_stage,
        "sector": user.sector,
        "bio": user.bio,
        "profile_image": user.profile_image,
        "language_preference": user.language_preference,
        "created_at": user.created_at,
    }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**user_dict)
    }

@router.post("/login-json", response_model=Token)
async def login_json(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """Login with JSON body (alternative to form data)"""
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    
    # Convert is_active string to boolean for response
    user_dict = {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active == "true" if isinstance(user.is_active, str) else bool(user.is_active),
        "business_stage": user.business_stage,
        "sector": user.sector,
        "bio": user.bio,
        "profile_image": user.profile_image,
        "language_preference": user.language_preference,
        "created_at": user.created_at,
    }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**user_dict)
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information"""
    # Convert is_active string to boolean for response
    user_dict = {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active == "true" if isinstance(current_user.is_active, str) else bool(current_user.is_active),
        "business_stage": current_user.business_stage,
        "sector": current_user.sector,
        "bio": current_user.bio,
        "profile_image": current_user.profile_image,
        "language_preference": current_user.language_preference,
        "created_at": current_user.created_at,
    }
    
    return UserResponse(**user_dict)

