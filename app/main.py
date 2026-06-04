from fastapi.middleware.cors import CORSMiddleware
from .middleware.logging import LoggingMiddleware
from app.core.config import settings
from app.core.dependencies import get_current_user
from fastapi import FastAPI

from app.api_router.auth_api import router as auth_router
from app.api_router.institute_api import router as institute_router

app = FastAPI(
    title=settings.APP_NAME,)

app.add_middleware(
    LoggingMiddleware
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
                   )

app.include_router(auth_router)
app.include_router(institute_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Edureon API"}