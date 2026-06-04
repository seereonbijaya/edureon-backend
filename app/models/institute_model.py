from sqlalchemy import Column, String, Boolean, BigInteger, Text, Integer, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class Institute(Base):
    __tablename__ = "institutes"

    id                  = Column(BigInteger, primary_key=True, autoincrement=True)
    institute_name      = Column(String(255), nullable=False)
    institute_code      = Column(String(255), unique=False)

    institute_type      = Column(String(255))

    board_affiliation   = Column(String(100))
    academic_year       = Column(String(20))

    brand_primary_color = Column(String(20))
    logo_url            = Column(String(500))

    street_address      = Column(Text)

    city                = Column(String(100))
    state               = Column(String(100))
    pin_code            = Column(String(20))
    country             = Column(String(100))

    phone               = Column(String(20))
    email               = Column(String(255))
    website             = Column(String(255))

    principal_name      = Column(String(255))
    principal_phone     = Column(String(20))

    admin_contact_name  = Column(String(255))
    admin_phone         = Column(String(20))

    gst_number          = Column(String(50))
    pan_number          = Column(String(50))

    is_active           = Column(Boolean, default=True)
    # created_at          = Column(DateTime, default=func.now())
    is_deleted           = Column(Boolean, default=False, nullable=False)
    created_by           = Column(Integer)
    updated_by           = Column(Integer)
    created_at           = Column(DateTime, server_default=func.now())
    updated_at           = Column(DateTime, server_default=func.now(), onupdate=func.now())
    document_ids = Column(JSON, default=list, nullable=True)
