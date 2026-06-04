from pydantic import BaseModel, Field
from typing import Optional, List

class InstituteCreate(BaseModel):
    institute_name: str
    institute_code: str

    institute_type: Optional[str]
    board_affiliation: Optional[str]
    academic_year: Optional[str]

    brand_primary_color: Optional[str]
    logo_url: Optional[str]

    street_address: Optional[str]

    city: Optional[str]
    state: Optional[str]
    pin_code: Optional[str]
    country: Optional[str]

    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]

    principal_name: Optional[str]
    principal_phone: Optional[str]

    admin_contact_name: Optional[str]
    admin_phone: Optional[str]
    document_ids: Optional[List[int]] = []

    gst_number: Optional[str]
    pan_number: Optional[str]



class InstituteUpdate(BaseModel):
    institute_name: Optional[str] = None
    institute_code: Optional[str] = None
    is_active: Optional[bool] = None
    document_ids: Optional[List[int]] = []
    

class InstituteResponse(BaseModel):
    id: int
    institute_name: str
    institute_code: str
    # is_active: bool

    class Config:
        from_attributes = True

