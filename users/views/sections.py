from typing import Optional

from sqlalchemy.orm import Session

from db import models
from users.schemas import sections as schemas


class Section:
    @staticmethod
    def get_list(page: Optional[int],
                 limit: Optional[int],
                 db: Session):
        if page and limit:
            return db.query(models.Section).offset(limit * (page - 1)).limit(limit).all()
        return db.query(models.Section).all()

    @staticmethod
    def get_by_id(db: Session, section_id: int):
        return db.query(models.Section).filter(models.Section.id == section_id).first()

    @staticmethod
    def create(db: Session, section: schemas.SectionCreate):
        db_section = models.Section(**section.dict())
        db.add(db_section)
        db.commit()
        db.refresh(db_section)
        return db_section

    @staticmethod
    def update(db: Session, db_section: models.Section, section: schemas.SectionUpdate):
        for key, value in section.dict().items():
            if value is not None:
                setattr(db_section, key, value)
        db.commit()
        return db_section

    @staticmethod
    def delete(db: Session, section_id: int):
        """ get section by id and delete all permissions related to it than delete section """
        db.query(models.Permission).filter(models.Permission.section_id == section_id).delete()
        db.query(models.Section).filter(models.Section.id == section_id).delete()
        db.commit()
        return {"success": "Section deleted successfully with all permissions related to it"}
