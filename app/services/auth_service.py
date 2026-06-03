from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    def register(
        db: Session,
        payload
    ):

        existing_user = (
            db.query(User)
            .filter(
                User.email == payload.email
            )
            .first()
        )

        if existing_user:
            raise Exception(
                "Email already exists"
            )

        user = User(
            name=payload.name,
            email=payload.email,
            password=hash_password(
                payload.password
            ),
            user_type="SUPER_ADMIN"
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str
    ):

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:
            raise Exception(
                "Invalid credentials"
            )

        if not verify_password(
            password,
            user.password
        ):
            raise Exception(
                "Invalid credentials"
            )

        token = create_access_token(
            {
                "user_id": user.id,
                "email": user.email,
                "user_type": user.user_type
            }
        )

        return token
