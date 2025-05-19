from fastapi import FastAPI
from routers.user_router import user_router
from fastapi.middleware.cors import CORSMiddleware

from db.db import BaseDBModel
from routers.proyectoPPS_router import proyecto_router


app = FastAPI()
BaseDBModel.metadata.create_all(bind=BaseDBModel.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""], 
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

#Register the user router
app.include_router(user_router)
app.include_router(proyecto_router)