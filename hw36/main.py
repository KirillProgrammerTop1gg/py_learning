from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from fastapi import Depends, FastAPI, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from db import Participant, get_db
import string

app = FastAPI()


class ParticipantCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        description="The name of the participant",
        json_schema_extra={"example": "nick"},
    )
    email: EmailStr = Field(
        ...,
        description="The email of the participant",
        json_schema_extra={"example": "example@test.com"},
    )
    event: str = Field(
        ...,
        min_length=2,
        description="The name of the event where the participant go",
        json_schema_extra={"example": "yoga"},
    )
    age: int = Field(
        ...,
        ge=12,
        le=120,
        description="The age of the participant",
        json_schema_extra={"example": "17"},
    )

    @field_validator("name")
    @classmethod
    def no_digits(cls, v: str) -> str:
        if any(map(lambda x: x in string.digits, v)):
            raise ValueError("Name shouldn't have digits")
        return v


class ParticipantResponse(ParticipantCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(
        ...,
        description="The id of the participant",
        json_schema_extra={"example": "23"},
    )


@app.post("/participants/", response_model=ParticipantResponse, status_code=201)
async def create_participant(
    participant_data: ParticipantCreate, db: AsyncSession = Depends(get_db)
):
    new_participant = Participant(**participant_data.model_dump())
    db.add(new_participant)
    try:
        await db.commit()
        await db.refresh(new_participant)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409, detail="Participant with this email already exists"
        )

    return new_participant


@app.get("/participants/event/{event_name}", response_model=list[ParticipantResponse])
async def get_participants_by_event(
    event_name: str = Path(..., description="The name of the event"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Participant).where(Participant.event == event_name)
    result = await db.execute(stmt)
    participants_by_event = result.scalars().all()
    if not participants_by_event:
        raise HTTPException(
            status_code=404, detail=f"No participants found for event '{event_name}'"
        )
    return participants_by_event
