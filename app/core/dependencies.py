from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from app.core.config import settings
from jose import jwt

security = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )
        return payload
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    # return token


def require_permission(permission: str):
    def checker(user=Depends(get_current_user)):
        permissions = user.get("permissions", [])
        if permission not in permissions:
            raise HTTPException(
                status_code=403,
                detail="Permission Denied"
            )
        return user
    return checker
