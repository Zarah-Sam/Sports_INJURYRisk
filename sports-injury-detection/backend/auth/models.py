"""
Authentication Models and Schemas
"""
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserRole(str, Enum):
    ATHLETE = "athlete"
    COACH = "coach"
    PHYSIOTHERAPIST = "physiotherapist"
    SPORTS_SCIENTIST = "sports_scientist"
    ADMINISTRATOR = "administrator"

class UserBase(BaseModel):
    id: str
    email: str
    full_name: str
    role: UserRole
    avatar_url: Optional[str] = None
    athlete_id: Optional[str] = None

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserBase

class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[UserRole] = None
