from sqlalchemy import Column, column, BigInteger, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    institute_id = Column(BigInteger, primary_key=False, index=True)
    name = Column(String(255), primary_key=False, index=True)
    email = Column(String(255), primary_key=False, index=True)
    password = Column(String(255), primary_key=False, index=False)
    user_type = Column(String(255), primary_key=False, index=False)
    is_active = Column(Boolean, primary_key=False, index=False)

    created_at = Column(BigInteger, primary_key=False, index=False)
    created_by = Column(BigInteger, primary_key=False, index=False)
    updated_at = Column(BigInteger, primary_key=False, index=False)
    updated_by = Column(BigInteger, primary_key=False, index=False)
    deleted_at = Column(BigInteger, primary_key=False, index=False)
    deleted_by = Column(BigInteger, primary_key=False, index=False)
    is_deleted = Column(Boolean, primary_key=False, index=False)
