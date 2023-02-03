from typing import Optional

from sqlalchemy.orm import Session

from db import models
from crud_models.schemas import ticket_classes as schemas


class TicketClass:
    @staticmethod
    def get_list(db: Session,
                 page: Optional[int],
                 limit: Optional[int]):
        if page and limit:
            return db.query(models.TicketClass).offset(limit * (page - 1)).limit(limit).all()
        return db.query(models.TicketClass).all()

    @staticmethod
    def get_by_id(db: Session, ticket_class_id: int):
        return db.query(models.TicketClass).filter(models.TicketClass.id == ticket_class_id).first()

    @staticmethod
    def create(db: Session, ticket_class: schemas.TicketClassCreate):
        db_ticket_class = models.TicketClass(**ticket_class.dict())
        db.add(db_ticket_class)
        db.commit()
        db.refresh(db_ticket_class)
        return db_ticket_class

    @staticmethod
    def update(db: Session,
               db_ticket_class: models.TicketClass,
               ticket_class: schemas.TicketClassUpdate):
        for key, value in ticket_class.dict().items():
            if value is not None:
                setattr(db_ticket_class, key, value)
        db.commit()
        return db_ticket_class

    @staticmethod
    def delete(db: Session, db_ticket_class: models.TicketClass):
        db.delete(db_ticket_class)
        db.commit()
        return {"message": "Ticket class deleted successfully"}
