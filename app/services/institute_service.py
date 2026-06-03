from app.models.institute import Institute
from sqlalchemy.orm import Session

from app.models.institute_document import InstituteDocument

class InstituteService:

    @staticmethod
    def create_institute(
        db: Session, 
        institute_data: dict,
        documents: list,
        created_by: int
        ):

        institute = Institute(
            **institute_data,
            created_by=created_by,
            updated_by=created_by
            )

        db.add(institute)
        db.commit()
        db.refresh(institute)

        for document in documents:
            document = InstituteDocument(
                institute_id=institute.id,
                document_name=document["document_name"],
                document_type=document["document_type"],
                file_path=document["file_path"],
                created_by=created_by,
                updated_by=created_by
            )
            db.add(document)
        db.commit()
        return institute
    
    @staticmethod
    def get_all(db):
        return db.query(Institute).filter(Institute.is_deleted == False).all()
    
    
    @staticmethod
    def get_by_id(db, institute_id):
        return db.query(Institute).filter(
            Institute.id == institute_id,
            Institute.is_deleted == False
        ).first()
    
    @staticmethod
    def update_institute(db, institute_id, payload):
        institute = db.query(Institute).filter(
            Institute.id == institute_id
        ).first()

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(institute, key, value)

        db.commit()
        db.refresh(institute)
        return institute
    
    @staticmethod
    def delete_institute(db, institute_id):
        institute = db.query(Institute).filter(
            Institute.id == institute_id
        ).first()
        institute.is_deleted = True
        db.commit()

        return True
    