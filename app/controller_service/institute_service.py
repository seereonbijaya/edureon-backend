from sqlalchemy.orm import Session
from app.models.institute_model import Institute
from app.models.institute_document_model import InstituteDocument

class InstituteService:

    @staticmethod
    def create_institute(
        db:             Session,
        institute_data: dict,
        documents:      list,
        created_by:     int
    ):
        institute = Institute(
            **institute_data,
            created_by=created_by,
            updated_by=created_by,
            document_ids=[]          # start with empty list
        )
        db.add(institute)
        db.flush()                   # get institute.id without full commit

        # insert each document record and collect IDs
        doc_ids = []
        for doc in documents:
            record = InstituteDocument(
                institute_id=  institute.id,
                document_name= doc["document_name"],
                document_type= doc["document_type"],
                file_name=     doc["file_name"],
                file_path=     doc["file_path"],
                file_size=     doc["file_size"],
                mime_type=     doc["mime_type"],
                created_by=    created_by,
                updated_by=    created_by,
            )
            db.add(record)
            db.flush()               # get record.id

            doc_ids.append(record.id)

        # UPDATED: write document ID list back to institute row
        institute.document_ids = doc_ids

        db.commit()
        db.refresh(institute)
        return institute

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Institute)
            .filter(Institute.is_deleted == False)
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, institute_id: int):
        return (
            db.query(Institute)
            .filter(
                Institute.id == institute_id,
                Institute.is_deleted == False
            )
            .first()
        )

    @staticmethod
    def update_institute(db: Session, institute_id: int, payload):
        institute = db.query(Institute).filter(
            Institute.id == institute_id
        ).first()
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(institute, key, value)
        db.commit()
        db.refresh(institute)
        return institute

    @staticmethod
    def delete_institute(db: Session, institute_id: int):
        institute = db.query(Institute).filter(
            Institute.id == institute_id
        ).first()
        institute.is_deleted = True
        db.commit()
        return True
    
