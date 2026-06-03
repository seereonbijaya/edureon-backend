# from sqlalchemy import Column, String, BigInteger, ForeignKey
# from app.database import Base
# from sqlalchemy.orm import func

# class InstituteDocument(Base):
#     __tablename__ = "institute_documents"

#     id = Column(BigInteger, primary_key=True)
#     institute_id = Column(BigInteger, ForeignKey("institutes.id"))

#     document_type = Column(String(255))
#     document_name = Column(String(255))

#     file_name = Column(String(255))
#     file_path = Column(String(1000))
#     file_size = Column(BigInteger)

#     mime_type = Column(String(255))

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base


class InstituteDocument(Base):
    __tablename__ = "institute_documents"

    id = Column(Integer, primary_key=True, index=True)

    institute_id = Column(
        Integer,
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False
    )

    document_name = Column(String(255))

    document_type = Column(String(100))

    file_path = Column(String(500))

    created_by = Column(Integer)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )