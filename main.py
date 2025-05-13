from fastapi import FastAPI
from routers.user_router import user_router

app = FastAPI()

# Register the user router
app.include_router(user_router)