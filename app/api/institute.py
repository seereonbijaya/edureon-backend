from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.file_upload import save_file
from app.models import institute
from app.schemas.institute import InstituteResponse, InstituteUpdate, InstituteCreate
from app.services.institute_service import InstituteService
from app.core.dependencies import require_permission, get_current_user
import os
import uuid

from typing import List, Optional, Annotated
from app.models.institute import Institute
from app.models.institute_document import InstituteDocument
import shutil


router = APIRouter(
    prefix="/institutes",
    tags=["Institutes"]
)

# @router.post("/")
# def create_institute(
#     name: str = Form(...),
#     institute_code: str = Form(...),
#     institute_type: str = Form(...),
#     board_affiliation: str = Form(None),
#     academic_year: str = Form(None),
#     brand_primary_color: str = Form(None),
#     street_address: str = Form(None),
#     city: str = Form(None),
#     state: str = Form(None),
#     pin_code: str = Form(None),
#     country: str = Form(None),
#     phone: str = Form(None),
#     email: str = Form(None),
#     website: str = Form(None),
#     principal_name: str = Form(None),
#     principal_phone: str = Form(None),
#     admin_contact_name: str = Form(None),
#     admin_phone: str = Form(None),
#     gst_number: str = Form(None),
#     pan_number: str = Form(None),

#     logo: UploadFile = File(None),

#     documents: list[UploadFile] = File(default=[]),

#     db: Session = Depends(get_db),

#     current_user=Depends(get_current_user)
# ):
#     logo_path = None

#     if logo:

#         os.makedirs(
#             "uploads/logo",
#             exist_ok=True
#         )

#         ext = logo.filename.split(".")[-1]

#         file_name = f"{uuid.uuid4()}.{ext}"

#         logo_path = f"uploads/logo/{file_name}"

#         with open(
#             logo_path,
#             "wb"
#         ) as buffer:

#             buffer.write(
#                 logo.file.read()
#             )

#     uploaded_docs = []

#     for doc in documents:

#         os.makedirs(
#             "uploads/documents",
#             exist_ok=True
#         )

#         ext = doc.filename.split(".")[-1]

#         file_name = f"{uuid.uuid4()}.{ext}"

#         path = f"uploads/documents/{file_name}"

#         with open(
#             path,
#             "wb"
#         ) as buffer:

#             buffer.write(
#                 doc.file.read()
#             )

#         uploaded_docs.append(
#             {
#                 "name": doc.filename,
#                 "path": path,
#                 "type": doc.content_type
#             }
#         )

#     institute = Institute(
#         name=name,
#         institute_code=institute_code,
#         institute_type=institute_type,
#         board_affiliation=board_affiliation,
#         academic_year=academic_year,
#         brand_primary_color=brand_primary_color,
#         logo_url=logo_path,
#         street_address=street_address,
#         city=city,
#         state=state,
#         pin_code=pin_code,
#         country=country,
#         phone=phone,
#         email=email,
#         website=website,
#         principal_name=principal_name,
#         principal_phone=principal_phone,
#         admin_contact_name=admin_contact_name,
#         admin_phone=admin_phone,
#         gst_number=gst_number,
#         pan_number=pan_number,
#         created_by=current_user["user_id"]
#     )

#     db.add(institute)

#     db.commit()

#     db.refresh(institute)

#     for doc in uploaded_docs:

#         document = InstituteDocument(
#             institute_id=institute.id,
#             document_name=doc["name"],
#             document_type=doc["type"],
#             file_path=doc["path"],
#             created_by=current_user["user_id"]
#         )

#         db.add(document)

#     db.commit()

#     return {
#         "success": True,
#         "message": "Institute created successfully",
#         "institute_id": institute.id
#     }

# ─── helper ── moved file saving to a reusable function ──────────────────────
# UPDATED: extracted file save logic into helper — avoids code duplication

def save_upload_file(upload_file: UploadFile, folder: str) -> str:
    os.makedirs(folder, exist_ok=True)
    ext = upload_file.filename.rsplit(".", 1)[-1] if "." in upload_file.filename else "bin"
    file_name = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(folder, file_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)  # ← UPDATED: shutil.copyfileobj is safer for large files
    return file_path


@router.post("/", response_model=dict)
def create_institute(
    # ── text fields (unchanged) ──────────────────────────────────────────────
    name: str = Form(...),
    institute_code: str = Form(...),
    institute_type: str = Form(...),
    board_affiliation: Optional[str] = Form(None),
    academic_year: Optional[str] = Form(None),
    brand_primary_color: Optional[str] = Form(None),
    street_address: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    pin_code: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    website: Optional[str] = Form(None),
    principal_name: Optional[str] = Form(None),
    principal_phone: Optional[str] = Form(None),
    admin_contact_name: Optional[str] = Form(None),
    admin_phone: Optional[str] = Form(None),
    gst_number: Optional[str] = Form(None),
    pan_number: Optional[str] = Form(None),

    # ── file fields ───────────────────────────────────────────────────────────
    logo: Optional[UploadFile] = File(None),

    # UPDATED: List[UploadFile] with File(None) — fixes 422 Unprocessable Content
    # Previously: list[UploadFile] = File(default=[]) — breaks in FastAPI < 0.109
    documents: Optional[List[UploadFile]] = File(None),
    # documents: Annotated[List[UploadFile], File(description="Upload multiple documents")] = []

    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # ── logo upload ───────────────────────────────────────────────────────────
    logo_path = None

    if logo and logo.filename:  # UPDATED: added filename check — prevents empty file object
        # UPDATED: validate logo mime type
        allowed_image_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}
        if logo.content_type not in allowed_image_types:
            raise HTTPException(
                status_code=400,
                detail=f"Logo must be an image. Got: {logo.content_type}"
            )
        logo_path = save_upload_file(logo, "uploads/logo")

    # ── documents upload ──────────────────────────────────────────────────────
    uploaded_docs = []

    # UPDATED: guard against None — when no files sent, documents is None not []
    if documents:
        allowed_doc_types = {
            "application/pdf",
            "image/jpeg", "image/png",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
        for doc in documents:
            if not doc.filename:  # UPDATED: skip empty file slots Swagger sends
                continue

            # UPDATED: validate document mime type
            if doc.content_type not in allowed_doc_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"Document '{doc.filename}' type not allowed: {doc.content_type}"
                )

            path = save_upload_file(doc, "uploads/documents")
            uploaded_docs.append({
                "name": doc.filename,
                "path": path,
                "type": doc.content_type
            })

    # ── create institute record ───────────────────────────────────────────────
    # UPDATED: wrapped in try/except — if DB fails, we still know what files were saved
    try:
        institute = Institute(
            name=name,
            institute_code=institute_code,
            institute_type=institute_type,
            board_affiliation=board_affiliation,
            academic_year=academic_year,
            brand_primary_color=brand_primary_color,
            logo_url=logo_path,
            street_address=street_address,
            city=city,
            state=state,
            pin_code=pin_code,
            country=country,
            phone=phone,
            email=email,
            website=website,
            principal_name=principal_name,
            principal_phone=principal_phone,
            admin_contact_name=admin_contact_name,
            admin_phone=admin_phone,
            gst_number=gst_number,
            pan_number=pan_number,
            created_by=current_user["user_id"]
        )

        db.add(institute)
        db.flush()  # UPDATED: flush first to get institute.id before committing docs

        # ── create document records ───────────────────────────────────────────
        for doc in uploaded_docs:
            document = InstituteDocument(
                institute_id=institute.id,
                document_name=doc["name"],
                document_type=doc["type"],
                file_path=doc["path"],
                created_by=current_user["user_id"]
            )
            db.add(document)

        db.commit()
        db.refresh(institute)

    except Exception as e:
        db.rollback()  # UPDATED: rollback on any DB error
        raise HTTPException(status_code=500, detail=f"Failed to create institute: {str(e)}")

    return {
        "success": True,
        "message": "Institute created successfully",
        "institute_id": str(institute.id),  # UPDATED: str() for UUID serialization safety
        "logo_url": logo_path,
        "documents_uploaded": len(uploaded_docs)  # UPDATED: useful feedback
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