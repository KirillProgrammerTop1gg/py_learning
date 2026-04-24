from fastapi import FastAPI

from routers.v1.animals import router as router_v1
from routers.v2.animals import router as router_v2
from routers.tasks import router as router_tasks

app = FastAPI()

app.include_router(router_v1)
app.include_router(router_v2)
app.include_router(router_tasks)
