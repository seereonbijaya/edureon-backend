from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.file_upload import save_file
from app.schemas.institute import InstituteResponse, InstituteUpdate, InstituteCreate
from app.services.institute_service import InstituteService
from app.core.dependencies import require_permission, get_current_user

router = APIRouter(
    prefix="/institutes",
    tags=["Institutes"]
)

@router.post("/")
def create_institute(
    name: str = Form(...),
    institute_code: str = Form(...),
    institute_type: str = Form(...),
    board_affiliation: str = Form(None),
    academic_year: str = Form(None),
    brand_primary_color: str = Form(None),
    street_address: str = Form(None),
    city: str = Form(None),
    state: str = Form(None),
    pin_code: str = Form(None),
    country: str = Form(None),
    phone: str = Form(None),
    email: str = Form(None),
    website: str = Form(None),
    principal_name: str = Form(None),
    principal_phone: str = Form(None),
    admin_contact_name: str = Form(None),
    admin_phone: str = Form(None),
    gst_number: str = Form(None),
    pan_number: str = Form(None),
    logo: UploadFile = File(None),
    documents: list[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    logo_path = None
    if logo:
        logo_path = save_file(logo,
                              "uploads/institute_logo"
                              )
    uploaded_documents = []

    for doc in documents:

        path = save_file(
            doc,
            "uploads/institute_documents"
        )

        uploaded_documents.append({
            "document_name": doc.filename,
            "document_type": doc.content_type,
            "file_path": path
        })
        institute_data = {

        "name": name,
        "institute_code": institute_code,
        "institute_type": institute_type,
        "board_affiliation": board_affiliation,
        "academic_year": academic_year,
        "brand_primary_color": brand_primary_color,
        "logo_url": logo_path,

        "street_address": street_address,
        "city": city,
        "state": state,
        "pin_code": pin_code,
        "country": country,

        "phone": phone,
        "email": email,
        "website": website,

        "principal_name": principal_name,
        "principal_phone": principal_phone,

        "admin_contact_name": admin_contact_name,
        "admin_phone": admin_phone,

        "gst_number": gst_number,
        "pan_number": pan_number
    }
    institute = InstituteService.create(
        db=db,
        institute_data=institute_data,
        documents=uploaded_documents,
        created_by=current_user.id
    )

    return {
        "success": True,
        "message": "Institute created successfully",
        "data": institute
    }
    

# @router.get("/")
# def get_all_institutes(
#     db=Depends(get_db)
# ):
#     return InstituteService.get_all(db)

# @router.get("/{institute_id}")
# def get_institute_by_id(
#     institute_id: int,
#     db=Depends(get_db)
# ):
#     return InstituteService.get_by_id(db, institute_id)


@router.put("/{institute_id}")
def update_institute(
    institute_id: int,
    payload: InstituteCreate,
    db=Depends(get_db)
):

    return InstituteService.update(
        db,
        institute_id,
        payload
    )

@router.delete("/{institute_id}")
def delete_institute(
    institute_id: int,
    db=Depends(get_db)
):
    return InstituteService.delete_institute(
        db, institute_id
    )