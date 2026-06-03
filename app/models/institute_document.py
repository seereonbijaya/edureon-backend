from sqlalchemy import Column, String, BigInteger, ForeignKey
from app.database import Base

class InstituteDocument(Base):
    __tablename__ = "institute_documents"

    id = Column(BigInteger, primary_key=True)
    institute_id = Column(BigInteger, ForeignKey("institutes.id"))

    document_type = Column(String(255))
    document_name = Column(String(255))

    file_name = Column(String(255))
    file_path = Column(String(1000))
    file_size = Column(BigInteger)

    mime_type = Column(String(255))
    