from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from db.database import get_db
from crud_models.schemas import ticket_classes as schemas
from crud_models.views.ticket_classes import TicketClass

routers = APIRouter()


@routers.get("/ticket_classes", response_model=list[schemas.TicketClass], tags=['ticket_classes'])
async def get_ticket_classes(page: Optional[int] = None,
                             limit: Optional[int] = None,
                             db: Session = Depends(get_db)):
    try:
        return TicketClass.get_list(db, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/ticket_class/{ticket_class_id}", tags=['ticket_classes'])
async def get_ticket_class(ticket_class_id: int,
                           db: Session = Depends(get_db)):
    db_ticket_class = TicketClass.get_by_id(db, ticket_class_id)
    if db_ticket_class is not None:
        return schemas.TicketClass.from_orm(db_ticket_class)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket class not found")


@routers.post("/ticket_class", tags=['ticket_classes'])
async def create_ticket_class(ticket_class: schemas.TicketClassCreate,
                              db: Session = Depends(get_db)):
    try:
        return schemas.TicketClass.from_orm(TicketClass.create(db, ticket_class))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/ticket_class/{ticket_class_id}", tags=["ticket_classes"])
async def update_ticket_class(ticket_class_id: int,
                              ticket_class: schemas.TicketClassUpdate,
                              db: Session = Depends(get_db)):
    db_ticket_class = TicketClass.get_by_id(db, ticket_class_id)
    if db_ticket_class is not None:
        return schemas.TicketClass.from_orm(TicketClass.update(db, db_ticket_class, ticket_class))
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket class not found")


@routers.delete("/ticket_class/{ticket_class_id}", tags=["ticket_classes"])
async def delete_ticket_class(ticket_class_id: int,
                              db: Session = Depends(get_db)):
    db_ticket_class = TicketClass.get_by_id(db, ticket_class_id)
    if db_ticket_class is not None:
        return TicketClass.delete(db, db_ticket_class)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket class not found")
