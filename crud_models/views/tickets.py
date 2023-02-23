import logging
import random
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from db import models
from crud_models.schemas import tickets as schemas
from datetime import datetime

from users.views.user_history import History


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
    def get_details_by_id(db: Session, ticket_id: int):
        query = db.execute(
            f"SELECT \
                        t.id, t.ticket_number, t.first_name, t.surname, t.middle_name, \
                        t.passport, t.passport_expires, t.dob, t.price, t.is_booked, t.comment, \
                        t.agent_id, t.luggage, \
                        company.name AS company_name, company.code AS company_code, \
                        json_build_object( \
                            'id', f.id, \
                            'flight_number', fg.flight_number, \
                            'departure_date', f.departure_date, \
                            'arrival_date', f.arrival_date, \
                            'from_city', c1.city_en, \
                            'from_airport_code', a1.code, \
                            'to_city', c2.city_en, \
                            'to_airport_code', a2.code \
                        ) AS flight, \
                        json_build_object( \
                            'id', country.id, \
                            'name_ru', country.country_ru, \
                            'name_en', country.country_en, \
                            'name_uz', country.country_uz,\
                            'code', country.code \
                        ) AS citizenship, \
                        json_build_object( \
                            'id', g.id, \
                            'gender_ru', g.gender_ru, \
                            'gender_en', g.gender_en, \
                            'gender_uz', g.gender_uz \
                        ) AS gender, \
                        json_build_object( \
                            'id', class.id, \
                            'name_ru', class.name_ru, \
                            'name_en', class.name_en, \
                            'name_uz', class.name_uz \
                        ) AS class, \
                        json_build_object( \
                            'id', status.id, \
                            'name_ru', status.name_ru, \
                            'name_en', status.name_en, \
                            'name_uz', status.name_uz \
                        ) AS status, \
                        t.created_at, t.updated_at, t.deleted_at \
                    FROM tickets t \
                    LEFT JOIN countries country ON country.id = t.citizenship \
                    LEFT JOIN genders g on t.gender_id = g.id \
                    LEFT JOIN ticket_classes class on t.class_id = class.id \
                    LEFT JOIN ticket_statuses status on t.status_id = status.id \
                    LEFT JOIN flights f on t.flight_id = f.id \
                    LEFT JOIN flight_guides fg on f.flight_guide_id = fg.id \
                    LEFT JOIN companies company on fg.company_id = company.id \
                    LEFT JOIN airports a1 on fg.from_airport_id = a1.id \
                    LEFT JOIN airports a2 on fg.to_airport_id = a2.id \
                    LEFT JOIN cities c1 on a1.city_id = c1.id \
                    LEFT JOIN cities c2 on a2.city_id = c2.id \
                    WHERE t.id = {ticket_id} "
        )

        return query.first()

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
            if hard or soft:
                db_ticket.is_booked = True
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

            # add to history this ticket
            History.create(db, user_id=user_id, action="create ticket", extra_info=f'Ticket {db_ticket.id} created')

            return {"message": "Ticket created successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ticket has trouble creating")

    @staticmethod
    def cancel(db: Session, ticket_cancel: schemas.TicketCancel, user_id: int):
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
        ticket.status_id = 3
        agent.balance -= ticket_cancel.fine
        agent.balance += ticket.price
        flight.left_seats += 1

        db.commit()

        db_agent_debt = models.AgentDebt(agent_id=agent.id, flight_id=flight.id, ticket_id=ticket.id,
                                         amount=ticket_cancel.fine, type='fine', comment=ticket_cancel.comment)
        db.add(db_agent_debt)
        db.commit()
        db.refresh(db_agent_debt)

        # add to history this ticket
        History.create(db, user_id=user_id, action="cancel ticket", extra_info=f'Ticket {ticket.id} canceled')

        return {"message": "Ticket deleted successfully and fine added to agent balance"}

    @staticmethod
    def update(db: Session,
               db_ticket: models.Ticket,
               ticket: schemas.TicketUpdate,
               db_flight: models.Flight,
               user_id: int,
               hard: bool = False,
               soft: bool = False):
        try:
            if db_ticket.agent_id != ticket.agent_id:
                new_ticket = models.Ticket()

                for key, value in db_ticket.__dict__.items():
                    if value is not None:
                        setattr(new_ticket, key, value)

                for key, value in ticket.dict().items():
                    if value is not None:
                        setattr(new_ticket, key, value)
                new_ticket.actor_id = user_id

                # create a new ticket and cancel old ticket
                Ticket.create(db, schemas.TicketCreate(**new_ticket.__dict__), db_flight, user_id, hard, soft)
                Ticket.cancel(db, schemas.TicketCancel(ticket_id=db_ticket.id, fine=0, currency=db_ticket.currency,
                                                       comment='Ticket was created wrong'))

            if db_ticket.luggage != ticket.luggage or hard or soft:
                query = db.query(models.FlightGuide.luggage, models.Agent.balance, models.Booking). \
                    join(models.FlightGuide, models.FlightGuide.id == db_flight.flight_guide_id). \
                    join(models.Agent, models.Agent.id == db_ticket.agent_id). \
                    join(models.Booking, models.Booking.id == db_ticket.booking_id). \
                    filter(models.Booking.agent_id == db_ticket.agent_id).first()

                luggage, balance, booking = query

                if hard or soft:
                    if booking.hard_block - 1 < 0 or booking.soft_block - 1 < 0:
                        raise ValueError('Agent has not enough block')
                    if hard:
                        booking.hard_block -= 1
                    if soft:
                        booking.soft_block -= 1
                    db_flight.left_seats += 1

                if not db_ticket.luggage and ticket.luggage:
                    db_ticket.price += luggage
                    balance -= luggage

                if db_ticket.luggage and not ticket.luggage:
                    db_ticket.price -= luggage
                    balance += luggage

            extra_info = ""
            for key, value in ticket.dict().items():
                if value is not None:
                    # add to extra_info data which is changed
                    if value != getattr(db_ticket, key):
                        extra_info += f"{key}: {getattr(db_ticket, key)} -> {value}\n"
                    setattr(db_ticket, key, value)

            if hard or soft:
                db_ticket.is_booked = True
            else:
                db_ticket.is_booked = False

            db_ticket.actor_id = user_id
            db.add(db_ticket)

            if hard or soft and db_ticket.luggage != ticket.luggage:
                db_agent_debt = models.AgentDebt(agent_id=db_ticket.agent_id, flight_id=db_flight.id,
                                                 ticket_id=db_ticket.id,
                                                 amount=db_ticket.price, type='purchase')

                db.add(db_agent_debt)
                db.commit()
                db.refresh(db_agent_debt)

            db.add(db_flight)
            db.commit()
            db.refresh(db_flight)

            # add to history this ticket
            History.create(db, user_id=user_id, action="update ticket",
                           extra_info=f'Ticket {db_ticket.id} updated:\n{extra_info}')

            return {"message": "Ticket updated successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ticket has trouble updating")
