import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Table,
    Text,
    Enum as SQLEnum,
)
from sqlalchemy.sql import func
from src.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

# --- Association table ---
skill_user_association = Table(
    "skill_user_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)


# --- Enums ---
class SkillLevel(enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"


class ExchangeStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"
    cancelled = "cancelled"


# --- Models ---
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=func.now()
    )

    # Relationships
    skills: Mapped[list["Skill"]] = relationship(
        back_populates="category_rel",
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    full_name: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    location: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    skills: Mapped[list["Skill"]] = relationship(
        secondary=skill_user_association,
        back_populates="users",
    )
    sent_exchanges: Mapped[list["Exchange"]] = relationship(
        foreign_keys="Exchange.sender_id",
        back_populates="sender",
    )
    received_exchanges: Mapped[list["Exchange"]] = relationship(
        foreign_keys="Exchange.receiver_id",
        back_populates="receiver",
    )
    given_reviews: Mapped[list["Review"]] = relationship(
        foreign_keys="Review.reviewer_id",
        back_populates="reviewer",
    )
    received_reviews: Mapped[list["Review"]] = relationship(
        foreign_keys="Review.reviewed_id",
        back_populates="reviewed",
    )


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    level: Mapped[SkillLevel] = mapped_column(SQLEnum(SkillLevel), nullable=False)
    can_teach: Mapped[bool] = mapped_column(Boolean, default=False)
    want_learn: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    category_rel: Mapped["Category"] = relationship(back_populates="skills")
    users: Mapped[list["User"]] = relationship(
        secondary=skill_user_association,
        back_populates="skills",
    )
    exchanges: Mapped[list["Exchange"]] = relationship(
        back_populates="skill",
    )


class Exchange(Base):
    __tablename__ = "exchanges"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), nullable=False)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ExchangeStatus] = mapped_column(
        SQLEnum(ExchangeStatus, name="exchange_status_enum"),
        default=ExchangeStatus.pending,
    )
    hours_proposed: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    sender: Mapped["User"] = relationship(
        foreign_keys=[sender_id],
        back_populates="sent_exchanges",
    )
    receiver: Mapped["User"] = relationship(
        foreign_keys=[receiver_id],
        back_populates="received_exchanges",
    )
    skill: Mapped["Skill"] = relationship(back_populates="exchanges")
    reviews: Mapped[list["Review"]] = relationship(back_populates="exchange")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"), nullable=False)
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reviewed_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)  # 1-5
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    exchange: Mapped["Exchange"] = relationship(back_populates="reviews")
    reviewer: Mapped["User"] = relationship(
        foreign_keys=[reviewer_id],
        back_populates="given_reviews",
    )
    reviewed: Mapped["User"] = relationship(
        foreign_keys=[reviewed_id],
        back_populates="received_reviews",
    )