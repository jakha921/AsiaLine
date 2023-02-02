import random

from starlette.responses import JSONResponse

from crud_models import schemas
from db import models

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from datetime import datetime
from fastapi import HTTPException, status
import traceback
import logging


class Country:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.Country).offset(offset).limit(limit).all()
        return db.query(models.Country).all()

    @staticmethod
    def get_by_id(db: Session, country_id: int):
        return db.query(models.Country).filter(models.Country.id == country_id).first()

    @staticmethod
    def create(db: Session, country: schemas.CountryCreate):
        db_country = models.Country(**country.dict())
        db.add(db_country)
        db.commit()
        db.refresh(db_country)
        return db_country

    @staticmethod
    def update(db: Session, db_country: models.Country, country: schemas.CountryUpdate):
        for key, value in country.dict().items():
            if value is not None:
                setattr(db_country, key, value)
        db.commit()
        return db_country

    @staticmethod
    def delete(db: Session, db_country: models.Country):
        for db_city in db_country.cities:
            City.delete(db, db_city)
        db.delete(db_country)
        db.commit()
        return db_country


class City:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.City).offset(offset).limit(limit).all()
        return db.query(models.City).all()

    @staticmethod
    def get_by_id(db: Session, city_id: int):
        return db.query(models.City).filter(models.City.id == city_id).first()

    @staticmethod
    def create(db: Session, city: schemas.CityCreate):
        db_city = models.City(**city.dict())
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city

    @staticmethod
    def update(db: Session, db_city: models.City, city: schemas.CityUpdate):
        for key, value in city.dict().items():
            if value is not None:
                setattr(db_city, key, value)
        db.commit()
        return db_city

    @staticmethod
    def delete(db: Session, db_city: models.City):
        try:
            for db_airport in db_city.airports:
                db.delete(db_airport)
            db.delete(db_city)
            db.commit()
            return db_city
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="City has trouble deleting")


class Airport:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.Airport).offset(offset).limit(limit).all()
        return db.query(models.Airport).all()

    @staticmethod
    def get_by_id(db: Session, airport_id: int):
        return db.query(models.Airport).filter(models.Airport.id == airport_id).first()

    @staticmethod
    def create(db: Session, airport: schemas.AirportCreate):
        db_airport = models.Airport(**airport.dict())
        db.add(db_airport)
        db.commit()
        db.refresh(db_airport)
        return db_airport

    @staticmethod
    def update(db: Session, db_airport: models.Airport, airport: schemas.AirportUpdate):
        for key, value in airport.dict().items():
            if value is not None:
                setattr(db_airport, key, value)
        db.commit()
        return db_airport

    @staticmethod
    def delete(db: Session, db_airport: models.Airport):
        try:
            db.delete(db_airport)
            db.commit()
            return db_airport
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Airport has trouble deleting")


class FlightPriceHistory:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.FlightPriceHistory).offset(offset).limit(limit).all()
        return db.query(models.FlightPriceHistory).all()

    @staticmethod
    def get_by_flight_id(db: Session, flight_id: int, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.FlightPriceHistory).filter(
                models.FlightPriceHistory.flight_id == flight_id).order_by(
                models.FlightPriceHistory.created_at.desc()).offset(offset).limit(limit).all()
        return db.query(models.FlightPriceHistory).filter(models.FlightPriceHistory.flight_id == flight_id).order_by(
            models.FlightPriceHistory.created_at.desc()).all()

    @staticmethod
    def create(db: Session, price: int, flight_id: int):
        db_price = models.FlightPriceHistory(new_price=price, flight_id=flight_id)
        db.add(db_price)
        db.commit()
        db.refresh(db_price)
        return db_price


class Ticket:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.Ticket) \
                .filter(models.Ticket.deleted_at == None,
                        models.Flight.id == models.Ticket.flight_id,
                        models.Flight.deleted_at == None,
                        models.Flight.departure_date >= datetime.now()) \
                .offset(offset).limit(limit).all()
        return db.query(models.Ticket). \
            filter(
            models.Ticket.deleted_at == None,
            models.Flight.id == models.Ticket.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()).all()

    @staticmethod
    def get_by_id(db: Session, ticket_id: int):
        return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    @staticmethod
    def update(db: Session, db_ticket: models.Ticket, ticket: schemas.TicketUpdate):
        for key, value in ticket.dict().items():
            if value is not None:
                setattr(db_ticket, key, value)
        db.commit()
        return db_ticket
    @staticmethod
    def create(db: Session, ticket: schemas.TicketCreate, db_flight: models.Flight, user_id: int, hard: bool = False,
               soft: bool = False):
        """ get from flight agent and him discount calculate price and create ticket than create agent debt history"""
        try:
            if hard or soft:
                query = db.query(models.Agent, models.Discount, models.Booking). \
                    join(models.Discount, models.Agent.discount_id == models.Discount.id). \
                    join(models.Booking, models.Agent.id == models.Booking.agent_id). \
                    filter(models.Agent.id == ticket.agent_id,
                           models.Discount.id == models.Agent.discount_id,
                           and_(models.Booking.agent_id == ticket.agent_id,
                                models.Booking.flight_id == db_flight.id)).first()
            else:
                query = db.query(models.Agent, models.Discount). \
                    join(models.Discount, models.Agent.discount_id == models.Discount.id). \
                    filter(models.Agent.id == ticket.agent_id,
                           models.Discount.id == models.Agent.discount_id).first()

            agent, discount, booking = models.Agent(), models.Discount(), models.Booking()

            if hard or soft:
                agent, discount, booking = query
            else:
                agent, discount = query["Agent"], query["Discount"]
            if agent is None:
                raise ValueError('Agent not found')
            print('agent', agent)
            if discount.amount is not None:
                price = db_flight.price - discount.amount
            else:
                price = db_flight.price

            price += ticket.luggage

            if not agent.is_on_credit:
                if agent.balance - price < 0:
                    raise ValueError('Agent has not enough balance')
                else:
                    agent.balance -= price
            else:
                agent.balance -= price

            if hard or soft:
                if hard:
                    qouta = booking.hard_block - 1
                    if qouta < 0:
                        raise ValueError('Agent has not enough hard block')
                    booking.hard_block -= 1
                if soft:
                    qouta = booking.soft_block - 1
                    if qouta < 0:
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

            db_agent_debt = models.AgentDebt(agent_id=db_ticket.agent_id, flight_id=db_flight.id, ticket_id=db_ticket.id,
                                             amount=db_ticket.price, type='purchase')
            db.add(db_agent_debt)
            db.commit()
            db.refresh(db_agent_debt)
            return {"message": "Ticket created successfully"}
        except ValueError as e:
            return JSONResponse(content={"error": str(e)}, status_code=400)
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=400, detail="Ticket not created")

    @staticmethod
    def delete(db: Session, db_ticket: models.Ticket):
        try:
            if db_ticket.deleted_at is not None:
                raise ValueError('Ticket already deleted')

            db_ticket.deleted_at = datetime.now()
            db.commit()

            db_flight = db.query(models.Flight).filter(models.Flight.id == db_ticket.flight_id).first()
            db_flight.left_seats += 1
            db.commit()

            return {"message": "Ticket deleted successfully and flight seats increased"}
        except ValueError as e:
            return JSONResponse(content={"error": str(e)}, status_code=400)
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ticket has trouble deleting")

    @staticmethod
    def cancel(db: Session, ticket_cancel: schemas.TicketCancel):
        try:
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
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Ticket canceling has trouble deleting")


class Booking:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.Booking) \
                .filter(
                models.Booking.deleted_at == None,
                models.Flight.id == models.Booking.flight_id,
                models.Flight.deleted_at == None,
                models.Flight.departure_date >= datetime.now()
            ).offset(offset).limit(limit).all()
        return db.query(models.Booking) \
            .filter(
            models.Booking.deleted_at == None,
            models.Flight.id == models.Booking.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()
        ).all()

    @staticmethod
    def get_by_id(db: Session, booking_id: int):
        return db.query(models.Booking). \
            filter(
            models.Booking.id == booking_id,
            models.Booking.deleted_at == None,
            models.Flight.id == models.Booking.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()
        ).first()

    @staticmethod
    def create(db: Session, booking: schemas.BookingCreate, flight: models.Flight):
        """ if booking created successfully, -1 from models Flight left_seats """
        if flight.left_seats - booking.hard_block - booking.soft_block < 0:
            return {'message': 'Flight has not enough seats'}

        flight.left_seats -= booking.hard_block + booking.soft_block
        db_booking = models.Booking(**booking.dict())
        db_booking.price = flight.price
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)

        return db_booking

    @staticmethod
    def update(db: Session, patch: schemas.BookingUpdate, booking: models.Booking, flight: models.Flight):
        """ find difference between old and new booking and update models Flight left_seats """

        diff = booking.hard_block + booking.soft_block - patch.hard_block - patch.soft_block
        flight.left_seats += diff
        if flight.left_seats < 0:
            return {'error': 'Flight has not enough seats'}

        for key, value in patch.dict().items():
            if value is not None:
                setattr(booking, key, value)
        db.commit()
        return booking

    @staticmethod
    def delete(db: Session, booking_id: int):
        try:
            db_booking = db.query(models.Booking, models.Agent, models.Flight). \
                filter(models.Booking.id == booking_id,
                       models.Agent.id == models.Booking.agent_id,
                       models.Flight.id == models.Booking.flight_id).first()

            booking = db_booking['Booking']
            agent = db_booking['Agent']
            flight = db_booking['Flight']

            if booking.deleted_at is not None:
                return {'message': 'Booking already deleted'}

            agent.balance += booking.price * booking.hard_block

            flight.left_seats += booking.hard_block + booking.soft_block

            booking.deleted_at = datetime.now()
            db.commit()

            return {"message": "Booking deleted successfully"}
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Booking has trouble deleting")


class Flight:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        try:
            if offset and limit:
                return db.query(models.Flight). \
                    filter(models.Flight.deleted_at == None,
                           models.Flight.departure_date >= datetime.now()). \
                    order_by(models.Flight.departure_date). \
                    offset(offset).limit(limit).all()
            return db.query(models.Flight). \
                filter(models.Flight.deleted_at == None,
                       models.Flight.departure_date >= datetime.now()). \
                order_by(models.Flight.departure_date).all()
        except Exception as e:
            print(e)

    @staticmethod
    def get_by_id(db: Session, flight_id: int):
        return db.query(models.Flight). \
            filter(
            models.Flight.id == flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()).first()

    @staticmethod
    def create(db: Session, flight: schemas.FlightCreate, user_id: int):
        db_flight = models.Flight(**flight.dict())
        db_flight.left_seats = flight.total_seats
        db_flight.actor_id = user_id
        db.add(db_flight)
        db.commit()
        db.refresh(db_flight)
        return db_flight

    @staticmethod
    def update(db: Session, db_flight: models.Flight, flight: schemas.FlightUpdate):
        for key, value in flight.dict().items():
            if value is not None:
                setattr(db_flight, key, value)
        db.commit()
        return db_flight

    @staticmethod
    def delete(db: Session, flight: models.Flight):
        """ get all bookings and tickets of this flight and delete them """
        try:
            db_ticket = db.query(models.Ticket).filter(models.Ticket.flight_id == flight.id).all()
            db_booking = db.query(models.Booking).filter(models.Booking.flight_id == flight.id).all()

            for ticket in db_ticket:
                ticket_schema = schemas.TicketCancel(
                    ticket_id=ticket.id,
                    fine=0,
                    currency='RUB',
                )
                Ticket.cancel(db, ticket_schema)
            for booking in db_booking:
                Booking.delete(db, booking.id)
            flight.deleted_at = datetime.now()
            db.commit()
            return {"message": "Flight deleted successfully and all tickets and bookings deleted for this flight"}
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Flight has trouble deleting")

    @staticmethod
    def get_flight_tickets(db: Session, flight_id: int):
        return db.query(models.Ticket).filter(
            models.Ticket.flight_id == flight_id,
            models.Ticket.deleted_at == None,
            models.Flight.id == models.Ticket.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()
        ).all()

    @staticmethod
    def set_on_sale_now(db: Session, db_flight: models.Flight):
        try:
            db_flight.on_sale = datetime.now()
            db.commit()
            return {"message": "Flight on sale now"}
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


class ScrapedPrice:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.ScrapedPrice) \
                .filter(
                models.Flight.id == models.ScrapedPrice.flight_id,
                models.Flight.deleted_at == None,
                models.Flight.departure_date >= datetime.now()
            ).offset(offset).limit(limit).all()
        return db.query(models.ScrapedPrice) \
            .filter(
            models.Flight.id == models.ScrapedPrice.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()).all()

    @staticmethod
    def get_by_id(db: Session, scraped_price_id: int):
        return db.query(models.ScrapedPrice).filter(
            models.ScrapedPrice.id == scraped_price_id,
            models.Flight.id == models.ScrapedPrice.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()
        ).first()

    @staticmethod
    def create(db: Session, scraped_price: schemas.ScrapedPriceCreate):
        db_scraped_price = models.ScrapedPrice(**scraped_price.dict())
        db.add(db_scraped_price)
        db.commit()
        db.refresh(db_scraped_price)
        return db_scraped_price

    @staticmethod
    def update(db: Session, db_scraped_price: models.ScrapedPrice, scraped_price: schemas.ScrapedPriceUpdate):
        for key, value in scraped_price.dict().items():
            if value is not None:
                setattr(db_scraped_price, key, value)
        db.commit()
        return db_scraped_price

    @staticmethod
    def delete(db: Session, db_scraped_price: models.ScrapedPrice):
        try:
            db.delete(db_scraped_price)
            db.commit()
            return {"message": "Scraped price deleted successfully"}
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Scraped Price has trouble deleting")


class Gender:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.Gender).offset(offset).limit(limit).all()
        return db.query(models.Gender).all()

    @staticmethod
    def get_by_id(db: Session, gender_id: int):
        return db.query(models.Gender).filter(models.Gender.id == gender_id).first()

    @staticmethod
    def create(db: Session, gender: schemas.GenderCreate):
        db_gender = models.Gender(**gender.dict())
        db.add(db_gender)
        db.commit()
        db.refresh(db_gender)
        return db_gender

    @staticmethod
    def update(db: Session, db_gender: models.Gender, gender: schemas.GenderUpdate):
        for key, value in gender.dict().items():
            if value is not None:
                setattr(db_gender, key, value)
        db.commit()
        return db_gender

    @staticmethod
    def delete(db: Session, gender_id: int):
        try:
            db_gender = db.query(models.Gender).filter(models.Gender.id == gender_id).first()
            if db_gender is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gender not found")
            db.delete(db_gender)
            db.commit()
            return {"message": "Gender deleted successfully"}
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Gender has trouble deleting")


class Refill:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.Refill).filter(models.Refill.deleted_at == None).offset(offset).limit(limit).all()
        return db.query(models.Refill).filter(models.Refill.deleted_at == None).all()

    @staticmethod
    def get_by_id(db: Session, refill_id: int):
        return db.query(models.Refill).filter(models.Refill.id == refill_id, models.Refill.deleted_at == None).first()

    @staticmethod
    def create(db: Session, refill: schemas.RefillCreate):
        db_refill = models.Refill(**refill.dict())

        agent = db.query(models.Agent).filter(models.Agent.id == refill.agent_id).first()
        agent.balance += refill.amount

        db.add(db_refill)
        db.commit()
        db.refresh(db_refill)
        return db_refill

    @staticmethod
    def update(db: Session, refill_id: int, refill: schemas.RefillUpdate):
        """ get refill and find difference between old and new amount than add it to agent balance """
        db_refill = db.query(models.Refill, models.Agent). \
            filter(models.Refill.id == refill_id,
                   models.Agent.id == models.Refill.agent_id).first()
        refill_db = db_refill['Refill']
        agent = db_refill['Agent']

        agent.balance += refill.amount - refill_db.amount

        for key, value in refill.dict().items():
            if value is not None:
                setattr(refill_db, key, value)

        db.commit()
        return refill_db

    @staticmethod
    def delete(db: Session, refill_id: int):
        try:
            refill_db = db.query(models.Refill, models.Agent). \
                filter(models.Refill.id == refill_id,
                       models.Agent.id == models.Refill.agent_id).first()

            db_refill = refill_db['Refill']
            agent = refill_db['Agent']

            if db_refill.deleted_at is not None:
                return {"message": "Refill already deleted"}

            agent.balance -= db_refill.amount

            db_refill.deleted_at = datetime.now()
            db.commit()
            return {"message": "Refill deleted successfully"}
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Refill has trouble deleting")


class AgentDebt:
    @staticmethod
    def get_list(db: Session, agent_id: int, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.AgentDebt).filter(models.AgentDebt.agent_id == agent_id).offset(offset).limit(
                limit).all()
        return db.query(models.AgentDebt).filter(models.AgentDebt.agent_id == agent_id).all()


class TicketClass:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.TicketClass).offset(offset).limit(limit).all()
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
    def update(db: Session, db_ticket_class: models.TicketClass, ticket_class: schemas.TicketClassUpdate):
        for key, value in ticket_class.dict().items():
            if value is not None:
                setattr(db_ticket_class, key, value)
        db.commit()
        return db_ticket_class

    @staticmethod
    def delete(db: Session, db_ticket_class: models.TicketClass):
        try:
            db.delete(db_ticket_class)
            db.commit()
            return {"message": "Ticket class deleted successfully"}
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="TicketClass has trouble deleting")
