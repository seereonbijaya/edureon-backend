
from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.institute_schema import InstituteResponse, InstituteUpdate
from app.controller_service.institute_service import InstituteService
from app.core.dependencies import get_current_user
import os
import uuid
import shutil

router = APIRouter(
    prefix="/institutes",
    tags=["Institutes"]
)

def save_upload_file(upload_file: UploadFile, folder: str) -> dict:
    os.makedirs(folder, exist_ok=True)
    ext = (
        upload_file.filename.rsplit(".", 1)[-1]
        if upload_file.filename and "." in upload_file.filename
        else "bin"
    )
    file_name = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(folder, file_name)

    upload_file.file.seek(0, 2)          
    file_size = upload_file.file.tell()  
    upload_file.file.seek(0)             
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return {
        "file_name": upload_file.filename,
        "file_path": file_path,
        "file_size": file_size,
        "mime_type": upload_file.content_type,
    }


@router.post("/", summary="Create Institute")
async def create_institute(
    institute_name: str = Form(...),
    institute_code: str = Form(...),
    institute_type:        Optional[str] = Form(None),
    board_affiliation:     Optional[str] = Form(None),
    academic_year:         Optional[str] = Form(None),
    brand_primary_color:   Optional[str] = Form(None),
    street_address:        Optional[str] = Form(None),
    city:                  Optional[str] = Form(None),
    state:                 Optional[str] = Form(None),
    pin_code:              Optional[str] = Form(None),
    country:               Optional[str] = Form(None),
    phone:                 Optional[str] = Form(None),
    email:                 Optional[str] = Form(None),
    website:               Optional[str] = Form(None),
    principal_name:        Optional[str] = Form(None),
    principal_phone:       Optional[str] = Form(None),
    admin_contact_name:    Optional[str] = Form(None),
    admin_phone:           Optional[str] = Form(None),
    gst_number:            Optional[str] = Form(None),
    pan_number:            Optional[str] = Form(None),

    logo: Optional[UploadFile] = File(None),

    documents: List[UploadFile] = File(default=[]),

    db:           Session = Depends(get_db),
    current_user: dict    = Depends(get_current_user),
):
    

    logo_path = None
    if logo and logo.filename:
        allowed_image_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}
        if logo.content_type not in allowed_image_types:
            raise HTTPException(
                status_code=400,
                detail=f"Logo must be an image. Got: {logo.content_type}"
            )
        result    = save_upload_file(logo, "uploads/institute_logo")
        logo_path = result["file_path"]

    uploaded_docs = []
    allowed_doc_types = {
        "application/pdf",
        "image/jpeg",
        "image/png",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    if documents:
        for doc in documents:
            if not doc or not doc.filename:
                continue
            if doc.content_type not in allowed_doc_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"'{doc.filename}' type not allowed: {doc.content_type}"
                )
            result = save_upload_file(doc, "uploads/institute_documents")
            uploaded_docs.append({
                "document_name": doc.filename,
                "document_type": doc.content_type,   # e.g. "application/pdf"
                "file_name":     result["file_name"],
                "file_path":     result["file_path"],
                "file_size":     result["file_size"],
                "mime_type":     result["mime_type"],
            })

    institute_data = {
        "institute_name":      institute_name,
        "institute_code":      institute_code,
        "institute_type":      institute_type,
        "board_affiliation":   board_affiliation,
        "academic_year":       academic_year,
        "brand_primary_color": brand_primary_color,
        "logo_url":            logo_path,
        "street_address":      street_address,
        "city":                city,
        "state":               state,
        "pin_code":            pin_code,
        "country":             country,
        "phone":               phone,
        "email":               email,
        "website":             website,
        "principal_name":      principal_name,
        "principal_phone":     principal_phone,
        "admin_contact_name":  admin_contact_name,
        "admin_phone":         admin_phone,
        "gst_number":          gst_number,
        "pan_number":          pan_number,
    }

    try:
        institute = InstituteService.create_institute(
            db=db,
            institute_data=institute_data,
            documents=uploaded_docs,
            created_by=current_user["user_id"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create institute: {str(e)}"
        )

    return {
        "success":            True,
        "message":            "Institute created successfully",
        "institute_id":       institute.id,
        "institute_name":     institute.institute_name,
        "logo_url":           institute.logo_url,
        "documents_uploaded": len(uploaded_docs),
        "document_ids":       institute.document_ids or [],
    }


@router.get("/", response_model=List[InstituteResponse])
def get_all_institutes(
    db:           Session = Depends(get_db),
    current_user: dict    = Depends(get_current_user),
):
    return InstituteService.get_all(db)


# GET /institutes/{institute_id}
@router.get("/{institute_id}", response_model=InstituteResponse)
def get_institute(
    institute_id: int,
    db:           Session = Depends(get_db),
    current_user: dict    = Depends(get_current_user),
):
    result = InstituteService.get_by_id(db, institute_id)
    if not result:
        raise HTTPException(status_code=404, detail="Institute not found")
    return result


@router.patch("/{institute_id}", response_model=InstituteResponse)
def update_institute(
    institute_id: int,
    payload:      InstituteUpdate,
    db:           Session = Depends(get_db),
    current_user: dict    = Depends(get_current_user),
):
    result = InstituteService.get_by_id(db, institute_id)
    if not result:
        raise HTTPException(status_code=404, detail="Institute not found")
    return InstituteService.update_institute(db, institute_id, payload)


@router.delete("/{institute_id}")
def delete_institute(
    institute_id: int,
    db:           Session = Depends(get_db),
    current_user: dict    = Depends(get_current_user),
):
    result = InstituteService.get_by_id(db, institute_id)
    if not result:
        raise HTTPException(status_code=404, detail="Institute not found")
    InstituteService.delete_institute(db, institute_id)
    return {"success": True, "message": "Institute deleted"}


