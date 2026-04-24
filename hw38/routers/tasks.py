import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Task ID", json_schema_extra={"example": 42})
    title: str = Field(
        ..., description="Task title", json_schema_extra={"example": "Buy books"}
    )
    done: bool = Field(
        ..., description="Is task completed", json_schema_extra={"example": False}
    )


FAKE_TASKS: dict[int, dict] = {
    1: {"id": 1, "title": "Buy books", "done": False},
    2: {"id": 2, "title": "Write report", "done": True},
    42: {"id": 42, "title": "Fix bug #42", "done": False},
}


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    if task_id > 1000:
        logger.warning(f"task_id={task_id} exceeds allowed limit (>1000)")
        raise HTTPException(
            status_code=422,
            detail=f"task_id={task_id} is out of range. Maximum allowed value is 1000.",
        )

    task = FAKE_TASKS.get(task_id)

    if task is None:
        logger.error(f"Task with id={task_id} not found")
        raise HTTPException(status_code=404, detail=f"Task with id={task_id} not found")

    logger.info(f"Task id={task_id} fetched successfully")
    return task
