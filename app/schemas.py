from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, RecordType


# Auth Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# User Response Schemas
class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


# Financial Record Schemas
class RecordBase(BaseModel):
    amount: float = Field(..., gt=0)
    type: RecordType
    category: str
    date: datetime
    description: Optional[str] = None


class RecordCreate(RecordBase):
    pass


class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[RecordType] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    description: Optional[str] = None


class RecordResponse(RecordBase):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


# Dashboard Schemas
class SummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float


class CategorySummary(BaseModel):
    category: str
    total: float


class TrendItem(BaseModel):
    month: str
    income: float
    expense: float
