from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.activity_router import activity_router
from routers.workplan_router import workplan_router
from routers.user_router import user_router
from routers.project_router import project_router

from db.db import BaseDBModel


app = FastAPI()
BaseDBModel.metadata.create_all(bind=BaseDBModel.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Register the user router
app.include_router(user_router)
app.include_router(project_router)
app.include_router(workplan_router)
app.include_router(activity_router)