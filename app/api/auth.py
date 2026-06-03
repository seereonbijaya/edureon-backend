from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.auth import (
    RegisterSchema,
    LoginSchema
)

from app.services.auth_service import (
    AuthService
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    payload: RegisterSchema,
    db: Session = Depends(get_db)
):

    user = AuthService.register(
        db,
        payload
    )

    return {
        "message": "Registered Successfully",
        "user_id": user.id
    }


@router.post("/login")
def login(payload: LoginSchema, db: Session = Depends(get_db)):


    token = AuthService.login(
        db,
        payload.email,
        payload.password
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
