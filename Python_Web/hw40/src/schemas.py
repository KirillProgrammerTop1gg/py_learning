from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from enum import Enum


# Enums
class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"


class ExchangeStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"
    cancelled = "cancelled"


# ───────────────────────────── Category schemas ──────────────────────────────


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Назва категорії")
    slug: str = Field(
        ...,
        min_length=2,
        max_length=100,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        description="URL-slug категорії (лише малі літери, цифри та дефіс)",
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Опис категорії"
    )
    icon: Optional[str] = Field(
        None, max_length=50, description="Назва іконки (напр. 'code', 'music')"
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    slug: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )
    description: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    skills_count: Optional[int] = None  # заповнюється окремо у repository

    model_config = ConfigDict(from_attributes=True)


class CategoryWithSkillsResponse(CategoryResponse):
    skills: List["SkillShortResponse"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# ───────────────────────────── User schemas ───────────────────────────────────


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None
    avatar_url: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=100)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    phone: str | None = None
    location: str | None = None

    model_config = ConfigDict(from_attributes=True)


# ───────────────────────────── Skill schemas ──────────────────────────────────


class SkillBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    category_id: int = Field(..., ge=1, description="ID категорії навички")
    level: SkillLevel


class SkillShortResponse(SkillBase):
    id: int
    can_teach: bool
    want_learn: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SkillCreate(SkillBase):
    can_teach: bool
    want_learn: bool

    @model_validator(mode="after")
    def check_teach_and_learn(self):
        if self.can_teach and self.want_learn:
            raise ValueError("Не можна одночасно вміти і хотіти вчитися одній навичці")
        return self


class SkillUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=500)
    category_id: Optional[int] = Field(None, ge=1)
    level: Optional[SkillLevel] = None
    can_teach: Optional[bool] = None
    want_learn: Optional[bool] = None


class SkillResponse(SkillBase):
    id: int
    can_teach: bool
    want_learn: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional["CategoryResponse"] = None
    users: List["UserResponse"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# ───────────────────────────── Exchange schemas ───────────────────────────────


class ExchangeBase(BaseModel):
    skill_id: int
    message: Optional[str] = Field(None, max_length=500)
    hours_proposed: int = Field(1, ge=1, le=10)


class ExchangeCreate(ExchangeBase):
    receiver_id: int


class ExchangeUpdate(BaseModel):
    status: Optional[ExchangeStatus] = None
    message: Optional[str] = None


class ExchangeResponse(ExchangeBase):
    id: int
    sender_id: int
    receiver_id: int
    status: ExchangeStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    sender: "UserResponse"
    receiver: "UserResponse"
    skill: "SkillResponse"

    model_config = ConfigDict(from_attributes=True)


# ───────────────────────────── Review schemas ─────────────────────────────────


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)


class ReviewCreate(ReviewBase):
    exchange_id: int


class ReviewResponse(ReviewBase):
    id: int
    exchange_id: int
    reviewer_id: int
    reviewed_id: int
    created_at: datetime
    reviewer: "UserResponse"
    reviewed: "UserResponse"

    model_config = ConfigDict(from_attributes=True)


# Update forward references
CategoryResponse.model_rebuild()
SkillShortResponse.model_rebuild()
CategoryWithSkillsResponse.model_rebuild()
UserResponse.model_rebuild()
SkillResponse.model_rebuild()
ExchangeResponse.model_rebuild()
ReviewResponse.model_rebuild()
