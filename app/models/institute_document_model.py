from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func

from app.database import Base


class InstituteDocument(Base):
    __tablename__ = "institute_documents"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    institute_id = Column(
        BigInteger,
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    document_type = Column(
        String(100),
        nullable=False
    )

    document_name = Column(
        String(255),
        nullable=True
    )

    file_name = Column(
        String(255),
        nullable=True
    )

    file_path = Column(
        String(1000),
        nullable=True
    )

    file_size = Column(
        BigInteger,
        nullable=True
    )

    mime_type = Column(
        String(100),
        nullable=True
    )

    created_by = Column(
        BigInteger,
        nullable=True
    )

    updated_by = Column(
        BigInteger,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    is_deleted = Column(
        Boolean,
        default=False
    )

    deleted_at = Column(
        DateTime,
        nullable=True
    )