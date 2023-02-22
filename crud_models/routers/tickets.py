from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from crud_models.views.flights import Flight
from db.database import get_db
from crud_models.schemas import tickets as schemas
from crud_models.views.tickets import Ticket
from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions, get_user_id

routers = APIRouter()


@routers.get("/tickets", response_model=list[schemas.Ticket], tags=["tickets"])
async def get_tickets(page: Optional[int] = None,
                      limit: Optional[int] = None,
                      jwt: dict = Depends(JWTBearer()),
                      db: Session = Depends(get_db)):
    """
    Get all tickets where ticket and flight are not deleted and flight departure date is greater than current date
    """
    if not check_permissions("get_tickets", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        return Ticket.get_list(db, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")


@routers.get("/ticket/{ticket_id}", response_model=schemas.Ticket, tags=["tickets"])
async def get_ticket(ticket_id: int,
                     jwt: dict = Depends(JWTBearer()),
                     db: Session = Depends(get_db)):
    """ Get ticket by id where ticket and flight are not deleted and flight departure date is greater
    than current date """
    if not check_permissions("get_ticket", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_ticket = Ticket.get_by_id(db, ticket_id)
        if db_ticket is None:
            raise ValueError("Ticket not found")
        return db_ticket
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@routers.get("/ticket/details/{ticket_id}", tags=["tickets"])
async def get_ticket_details(ticket_id: int,
                                jwt: dict = Depends(JWTBearer()),
                                db: Session = Depends(get_db)):
        """ Get ticket details by id where ticket and flight are not deleted and flight departure date is greater
        than current date """
        if not check_permissions("get_ticket_details", jwt):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

        try:
            db_ticket = Ticket.get_details_by_id(db, ticket_id)
            if db_ticket is None:
                raise ValueError("Ticket not found")
            return db_ticket
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@routers.post("/ticket", tags=["tickets"])
async def create_ticket(ticket: schemas.TicketCreate,
                        hard: bool = False,
                        soft: bool = False,
                        jwt: dict = Depends(JWTBearer()),
                        db: Session = Depends(get_db)):
    """
    Create ticket for flight\n
    **Rules:**\n
    * hard and soft cannot be true at the same time
    * if hard and soft are false,
     then ticket will be created from flight left seats quotes,
     if there are enough seats\n
    * if flight is not on sale, ticket will not be created
    * if flight is deleted, ticket will not be created
    * if flight departure date is less than current date, ticket will not be created
    * if flight left seats is less or equal to 0, ticket will not be created
    """
    if not check_permissions("create_ticket", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        if hard and soft:
            raise ValueError("hard and soft cannot be true at the same time")
        if ticket.flight_id is None:
            raise ValueError("flight_id is required")
        db_flight = Flight.get_by_id(db, ticket.flight_id)
        if db_flight is None or db_flight.deleted_at is not None or db_flight.on_sale > datetime.now() or \
                db_flight.departure_date < datetime.now():
            raise ValueError("Flight not found")
        if db_flight.left_seats <= 0:
            raise ValueError("Flight left seats is less or equal to 0")
        return Ticket.create(db, ticket, db_flight, get_user_id(jwt), hard, soft)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@routers.patch("/ticket/{ticket_id}", tags=["tickets"])
async def update_ticket(ticket_id: int,
                        ticket: schemas.TicketUpdate,
                        hard: bool = False,
                        soft: bool = False,
                        jwt: dict = Depends(JWTBearer()),
                        db: Session = Depends(get_db)):
    """
    Update ticket by id\n
    **Rules:**\n
    * ticket cannot be updated if flight is on sale
    * ticket cannot be updated if flight is deleted
    * ticket cannot be updated if flight departure date is less than current date
    * ticket cannot be updated if ticket is deleted
    """
    if not check_permissions("update_ticket", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # try:
    db_ticket = Ticket.get_by_id(db, ticket_id)
    if db_ticket.is_booked:
        raise ValueError("Ticket is booked you cannot change this ticket")
    db_flight = Flight.get_by_id(db, ticket.flight_id)
    if db_flight is None or db_flight.deleted_at is not None or db_flight.on_sale > datetime.now() or \
            db_flight.departure_date < datetime.now():
        raise ValueError("Flight not found")
    if db_ticket is None or db_ticket.deleted_at is not None or db_flight.departure_date < datetime.now():
        raise ValueError("Ticket not found")
    return Ticket.update(db, db_ticket, ticket, db_flight, get_user_id(jwt), hard, soft)
    # except ValueError as e:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@routers.post("/ticket/cancellation", tags=["tickets"])
async def cancel_ticket_add_to_agent_fine(ticket_cancel: schemas.TicketCancel,
                                          jwt: dict = Depends(JWTBearer()),
                                          db: Session = Depends(get_db)):
    """
    Cancel ticket and add fine to agent will bу added to flight left seats\n
    """
    if not check_permissions("cancel_ticket", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_ticket = Ticket.get_by_id(db, ticket_cancel.ticket_id)
        if db_ticket.deleted_at or db_ticket is None:
            raise ValueError("Ticket not found")
        return Ticket.cancel(db, ticket_cancel, get_user_id(jwt))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
