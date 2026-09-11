from fastapi import FastAPI, Query, HTTPException, Path
from pydantic import BaseModel, Field, UUID4
from typing import List
import uuid

app = FastAPI(title="Task Manager API", version="1.0.0")

tasks: dict[UUID4, dict] = {}


class Task(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="The name of the task",
        json_schema_extra={"example": "Do algebra HW"},
    )
    description: str = Field(
        ...,
        min_length=7,
        max_length=250,
        description="The description of the task",
        json_schema_extra={"example": "In book: 32.6, 32.8, 32.14, 32.18"},
    )


class TaskActionResponse(BaseModel):
    message: str = Field(
        ...,
        description="Message that describes action about task",
        json_schema_extra={"example": "Task created successfully"},
    )
    task_id: UUID4 = Field(
        ...,
        description="The task id in uuid v4",
        json_schema_extra={"example": "e6e82022-089f-46ed-822e-7907672d0236"},
    )


class TaskResponse(BaseModel):
    task_id: UUID4 = Field(
        ...,
        description="The task id in uuid v4",
        json_schema_extra={"example": "e6e82022-089f-46ed-822e-7907672d0236"},
    )
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="The name of the task",
        json_schema_extra={"example": "Do algebra HW"},
    )
    description: str = Field(
        ...,
        min_length=7,
        max_length=250,
        description="The description of the task",
        json_schema_extra={"example": "In book: 32.6, 32.8, 32.14, 32.18"},
    )


class AllTasksResponse(BaseModel):
    tasks: List[TaskResponse]


@app.post(
    "/tasks/",
    description="Endpoint to create task in list",
    status_code=201,
    response_model=TaskActionResponse,
)
def create_task(task: Task):
    if any(t["name"] == task.name for t in tasks.values()):
        raise HTTPException(
            status_code=409, detail="Task with this name already exists"
        )
    task_id = uuid.uuid4()
    tasks[task_id] = task.model_dump()
    return {"message": "Task created successfully", "task_id": task_id}


@app.put(
    "/tasks/{task_id}",
    description="Endpoint to update task in list",
    response_model=TaskActionResponse,
)
def update_task(task: Task, task_id: UUID4 = Path(..., description="task id")):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    if any(t["name"] == task.name and task_id != tid for tid, t in tasks.items()):
        raise HTTPException(status_code=409, detail="Task with this already exists")
    tasks[task_id] = task.model_dump()
    return {"message": "Task updated successfully", "task_id": task_id}


@app.delete(
    "/tasks/{task_id}",
    description="Endpoint to delete task from list",
    response_model=TaskActionResponse,
)
def delete_task(task_id: UUID4 = Path(..., description="task id")):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.pop(task_id)
    return {"message": "Task deleted successfully", "task_id": task_id}


@app.get(
    "/tasks/{task_id}",
    description="Endpoint to get task by id",
    response_model=TaskResponse,
)
def get_task_by_id(task_id: UUID4 = Path(..., description="task id")):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, **tasks[task_id]}


@app.get(
    "/tasks/",
    description="Endpoint to get all tasks",
    response_model=AllTasksResponse,
)
def get_all_tasks():
    return {
        "tasks": [
            {"task_id": task_id, **task_data} for task_id, task_data in tasks.items()
        ]
    }
