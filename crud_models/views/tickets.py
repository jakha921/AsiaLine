import logging
import random
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from db import models
from crud_models.schemas import tickets as schemas
from datetime import datetime


class Ticket:
    @staticmethod
    def get_list(db: Session, page: Optional[int], limit: Optional[int]):

        query = db.query(models.Ticket). \
            filter(
            models.Ticket.deleted_at == None,
            models.Flight.id == models.Ticket.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now())
        if page and limit:
            return query.offset(limit * (page - 1)).limit(limit).all()
        return query.all()

    @staticmethod
    def get_by_id(db: Session, ticket_id: int):
        return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    @staticmethod
    def create(db: Session, ticket: schemas.TicketCreate, db_flight: models.Flight, user_id: int, hard: bool = False,
               soft: bool = False):
        """ get from flight agent and him discount calculate price and create ticket than create agent debt history"""
        try:
            if hard or soft:
                query = db.query(models.Agent, models.Discount, models.Booking, models.FlightGuide). \
                    join(models.Discount, models.Agent.discount_id == models.Discount.id). \
                    join(models.Booking, models.Agent.id == models.Booking.agent_id). \
                    join(models.FlightGuide, models.FlightGuide.id == db_flight.flight_guide_id). \
                    filter(models.Agent.id == ticket.agent_id,
                           models.Discount.id == models.Agent.discount_id,
                           models.FlightGuide.id == db_flight.flight_guide_id,
                           and_(models.Booking.agent_id == ticket.agent_id,
                                models.Booking.flight_id == db_flight.id)).first()
            else:
                query = db.query(models.Agent, models.Discount, models.FlightGuide). \
                    join(models.Discount, models.Agent.discount_id == models.Discount.id). \
                    join(models.FlightGuide, models.FlightGuide.id == db_flight.flight_guide_id). \
                    filter(models.Agent.id == ticket.agent_id,
                           models.Discount.id == models.Agent.discount_id).first()

            agent, discount, booking, flight_guide = models.Agent(), models.Discount(), models.Booking(), \
                models.FlightGuide()

            if hard or soft:
                agent, discount, booking, flight_guide = query
            else:
                agent, discount, flight_guide = query["Agent"], query["Discount"], query["FlightGuide"]

            if agent is None:
                raise ValueError('Agent not found')

            if discount.amount is not None:
                price = db_flight.price - discount.amount
            else:
                price = db_flight.price

            if hard:
                price -= db_flight.price - booking.price

            if ticket.luggage:
                price += flight_guide.luggage

            if not agent.is_on_credit:
                if agent.balance - price < 0:
                    raise ValueError('Agent has not enough balance')
                else:
                    agent.balance -= price
            else:
                agent.balance -= price

            if hard or soft:
                if hard:
                    if booking.hard_block - 1 < 0:
                        raise ValueError('Agent has not enough hard block')
                    booking.hard_block -= 1
                if soft:
                    if booking.soft_block - 1 < 0:
                        raise ValueError('Agent has not enough soft block')
                    booking.soft_block -= 1
            else:
                if db_flight.left_seats - 1 < 0:
                    raise ValueError('Flight has not enough seats')
                db_flight.left_seats -= 1

            db_ticket = models.Ticket(**ticket.dict())
            db_ticket.price = price
            db_ticket.ticket_number = "WZ " + str(random.randint(10000000, 99999999))
            db_ticket.actor_id = user_id
            db.add(db_ticket)
            db.commit()
            db.refresh(db_ticket)

            db_agent_debt = models.AgentDebt(agent_id=db_ticket.agent_id, flight_id=db_flight.id,
                                             ticket_id=db_ticket.id,
                                             amount=db_ticket.price, type='purchase')
            db.add(db_agent_debt)
            db.commit()
            db.refresh(db_agent_debt)
            return {"message": "Ticket created successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ticket has trouble creating")

    @staticmethod
    def update(db: Session, db_ticket: models.Ticket, ticket: schemas.TicketUpdate, flight):
        if db_ticket.luggage != ticket.luggage:
            luggage_price = db.query(models.FlightGuide, models.Agent).\
                join(models.Agent, models.Agent.id == db_ticket.agent_id).\
                filter(models.FlightGuide.id == flight.flight_guide_id).first()

            if not db_ticket.luggage and ticket.luggage:
                db_ticket.price += luggage_price[0].luggage
                luggage_price[1].balance -= luggage_price[0].luggage

            if db_ticket.luggage and not ticket.luggage:
                db_ticket.price -= luggage_price[0].luggage
                luggage_price[1].balance += luggage_price[0].luggage

        for key, value in ticket.dict().items():
            if value is not None:
                setattr(db_ticket, key, value)
        db.commit()
        return db_ticket

    @staticmethod
    def cancel(db: Session, ticket_cancel: schemas.TicketCancel):
        db_ticket = db.query(
            models.Ticket, models.Agent, models.Flight). \
            filter(
            models.Ticket.id == ticket_cancel.ticket_id,
            models.Agent.id == models.Ticket.agent_id,
            models.Flight.id == models.Ticket.flight_id).first()

        ticket = db_ticket['Ticket']
        agent = db_ticket['Agent']
        flight = db_ticket['Flight']

        ticket.deleted_at = datetime.now()
        agent.balance -= ticket_cancel.fine
        agent.balance += ticket.price
        flight.left_seats += 1

        db.commit()

        db_agent_debt = models.AgentDebt(agent_id=agent.id, flight_id=flight.id, ticket_id=ticket.id,
                                         amount=ticket_cancel.fine, type='fine')
        db.add(db_agent_debt)
        db.commit()
        db.refresh(db_agent_debt)

        return {"message": "Ticket deleted successfully and fine added to agent balance"}
