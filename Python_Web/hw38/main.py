from fastapi import FastAPI

from Python_Web.hw38.routers.v1.animals import router as router_v1
from Python_Web.hw38.routers.v2.animals import router as router_v2
from Python_Web.hw38.routers.tasks import router as router_tasks

app = FastAPI()

app.include_router(router_v1)
app.include_router(router_v2)
app.include_router(router_tasks)
