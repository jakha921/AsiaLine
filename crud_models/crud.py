import random

from crud_models import schemas
from db import models

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
from typing import Optional
from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException, status
import traceback
import logging


class Country:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        print(min, max)
        if min and max:
            return db.query(models.Country).offset(min).limit(max).all()
        return db.query(models.Country).all()

    def get_by_id(db: Session, country_id: int):
        return db.query(models.Country).filter(models.Country.id == country_id).first()

    def create(db: Session, country: schemas.CountryCreate):
        db_country = models.Country(**country.dict())
        db.add(db_country)
        db.commit()
        db.refresh(db_country)
        return db_country

    def update(db: Session, country_id: int, country: schemas.CountryUpdate):
        db_country = db.query(models.Country).filter(models.Country.id == country_id).first()
        for key, value in country.dict().items():
            if value is not None:
                setattr(db_country, key, value)
        db.commit()
        return db_country

    def delete(db: Session, country_id: int):
        db_country = db.query(models.Country).filter(models.Country.id == country_id).first()
        if db_country is None:
            return {'message': 'Country not found'}
        db.delete(db_country)
        db.commit()
        return db_country


class City:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.City).offset(min).limit(max).all()
        return db.query(models.City).all()

    def get_by_id(db: Session, city_id: int):
        return db.query(models.City).filter(models.City.id == city_id).first()

    def create(db: Session, city: schemas.CityCreate):
        db_city = models.City(**city.dict())
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city

    def update(db: Session, city_id: int, city: schemas.CityUpdate):
        db_city = db.query(models.City).filter(models.City.id == city_id).first()
        for key, value in city.dict().items():
            if value is not None:
                setattr(db_city, key, value)
        db.commit()
        return db_city

    def delete(db: Session, city_id: int):
        try:
            db_city = db.query(models.City).filter(models.City.id == city_id).first()
            if db_city is None:
                return {'message': 'City not found'}
            else:
                db.delete(db_city)
                db.commit()
                return db_city
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


class Airport:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Airport).offset(min).limit(max).all()
        return db.query(models.Airport).all()

    def get_by_id(db: Session, airport_id: int):
        return db.query(models.Airport).filter(models.Airport.id == airport_id).first()

    def create(db: Session, airport: schemas.AirportCreate):
        db_airport = models.Airport(**airport.dict())
        db.add(db_airport)
        db.commit()
        db.refresh(db_airport)
        return db_airport

    def update(db: Session, airport_id: int, airport: schemas.AirportUpdate):
        db_airport = db.query(models.Airport).filter(models.Airport.id == airport_id).first()
        for key, value in airport.dict().items():
            if value is not None:
                setattr(db_airport, key, value)
        db.commit()
        return db_airport

    def delete(db: Session, airport_id: int):
        try:
            db_airport = db.query(models.Airport).filter(models.Airport.id == airport_id).first()
            if db_airport is None:
                return {'message': 'Airport not found'}
            else:
                db.delete(db_airport)
                db.commit()
                return db_airport
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


class FlightPriceHistory:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        print(min, max)
        if min and max:
            return db.query(models.FlightPriceHistory).offset(min).limit(max).all()
        return db.query(models.FlightPriceHistory).all()

    def get_by_flight_id(db: Session, flight_id: int, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.FlightPriceHistory).filter(
                models.FlightPriceHistory.flight_id == flight_id).order_by(
                models.FlightPriceHistory.created_at.desc()).offset(min).limit(max).all()
        return db.query(models.FlightPriceHistory).filter(models.FlightPriceHistory.flight_id == flight_id).order_by(
            models.FlightPriceHistory.created_at.desc()).all()

    def create(db: Session, price: int, flight_id: int):
        db_price = models.FlightPriceHistory(new_price=price, flight_id=flight_id)
        db.add(db_price)
        db.commit()
        db.refresh(db_price)
        return db_price


class Ticket:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Ticket) \
                .filter(models.Ticket.deleted_at == None,
                        models.Flight.id == models.Ticket.flight_id,
                        models.Flight.deleted_at == None,
                        models.Flight.departure_date >= datetime.now()) \
                .offset(min).limit(max).all()
        return db.query(models.Ticket). \
            filter(
            models.Ticket.deleted_at == None,
            models.Flight.id == models.Ticket.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()).all()

    def get_by_id(db: Session, ticket_id: int):
        return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    def create(db: Session, ticket: schemas.TicketCreate, db_flight: models.Flight, hard: bool = False,
               soft: bool = False):
        """ get from flight agent and him discount calculate price and create ticket than create agent debt history"""
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
            return {'message': 'Agent not found'}

        if discount.amount is not None:
            price = db_flight.price - discount.amount
        else:
            price = db_flight.price

        price += ticket.luggage

        if not agent.is_on_credit:
            if agent.balance - price < 0:
                return {'message': 'Agent has not enough on balance'}
            else:
                agent.balance -= price
        else:
            agent.balance -= price

        if hard or soft:
            if hard:
                qouta = booking.hard_block - 1
                if qouta < 0:
                    return {'message': 'Agent has not enough hard block'}
                booking.hard_block -= 1
            if soft:
                qouta = booking.soft_block - 1
                if qouta < 0:
                    return {'message': 'Agent has not enough soft block'}
                booking.soft_block -= 1
        else:
            if db_flight.left_seats - 1 < 0:
                return {'message': 'Flight has not enough seats'}
            db_flight.left_seats -= 1

        db_ticket = models.Ticket(**ticket.dict())
        db_ticket.price = price
        db_ticket.ticket_number = "WZ " + str(random.randint(10000000, 99999999))
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)

        db_agent_debt = models.AgentDebt(agent_id=db_ticket.agent_id, flight_id=db_flight.id, ticket_id=db_ticket.id,
                                         amount=db_ticket.price, type='purchase')
        db.add(db_agent_debt)
        db.commit()
        db.refresh(db_agent_debt)

        return {"message": "Ticket created successfully"}

    def update(db: Session, ticket_id: int, ticket: schemas.TicketUpdate):
        db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        for key, value in ticket.dict().items():
            if value is not None:
                setattr(db_ticket, key, value)
        db.commit()
        return db_ticket

    def delete(db: Session, ticket_id: int):
        try:
            db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
            if db_ticket is None:
                return {'error': 'Ticket not found'}
            if db_ticket.deleted_at is None:
                db_ticket.deleted_at = datetime.now()
            else:
                return {"message": "Ticket already deleted"}
            db.commit()

            db_flight = db.query(models.Flight).filter(models.Flight.id == db_ticket.flight_id).first()
            db_flight.left_seats += 1
            db.commit()

            return {"message": "Ticket deleted successfully"}
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

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
            print(agent.balance)

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

            print(agent.balance)

            return {"message": "Ticket deleted successfully and fine added to agent balance"}
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


class Booking:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Booking) \
                .filter(
                models.Booking.deleted_at == None,
                models.Flight.id == models.Booking.flight_id,
                models.Flight.deleted_at == None,
                models.Flight.departure_date >= datetime.now()
            ).offset(min).limit(max).all()
        return db.query(models.Booking) \
            .filter(
            models.Booking.deleted_at == None,
            models.Flight.id == models.Booking.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()
        ).all()

    def get_by_id(db: Session, booking_id: int):
        return db.query(models.Booking). \
            filter(
            models.Booking.id == booking_id,
            models.Booking.deleted_at == None,
            models.Flight.id == models.Booking.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()
        ).first()

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

    def update(db: Session, patch: schemas.BookingUpdate, booking: models.Booking, flight: models.Flight):
        """ find difference between old and new booking and update models Flight left_seats """
        print('before', flight.left_seats)

        diff = booking.hard_block + booking.soft_block - patch.hard_block - patch.soft_block
        print('diff', diff)
        flight.left_seats += diff
        if flight.left_seats < 0:
            return {'message': 'Flight has not enough seats'}

        for key, value in patch.dict().items():
            if value is not None:
                setattr(booking, key, value)
        db.commit()
        print('after', flight.left_seats)
        return booking

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
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


class Flight:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        try:
            if min and max:
                return db.query(models.Flight). \
                    filter(models.Flight.deleted_at == None,
                           models.Flight.departure_date >= datetime.now()). \
                    order_by(models.Flight.departure_date). \
                    offset(min).limit(max).all()
            return db.query(models.Flight). \
                filter(models.Flight.deleted_at == None,
                       models.Flight.departure_date >= datetime.now()). \
                order_by(models.Flight.departure_date).all()
        except Exception as e:
            print(e)

    def get_by_id(db: Session, flight_id: int):
        return db.query(models.Flight). \
            filter(
            models.Flight.id == flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()).first()

    def create(db: Session, flight: schemas.FlightCreate):
        db_flight = models.Flight(**flight.dict())
        db_flight.left_seats = flight.total_seats
        db.add(db_flight)
        db.commit()
        db.refresh(db_flight)
        return db_flight

    def update(db: Session, flight_id: int, flight: schemas.FlightUpdate):
        db_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
        for key, value in flight.dict().items():
            if value is not None:
                setattr(db_flight, key, value)
        db.commit()
        return db_flight

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
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    def get_flight_tickets(db: Session, flight_id: int):
        return db.query(models.Ticket).filter(models.Ticket.flight_id == flight_id).all()

    def set_on_sale_now(db: Session, flight_id: int, on_sale: bool = False):
        try:
            db_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
            if db_flight is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
            if on_sale:
                db_flight.on_sale = datetime.now()
            db.commit()
            return db_flight
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


class ScrapedPrice:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.ScrapedPrice).offset(min).limit(max).all()
        return db.query(models.ScrapedPrice).all()

    def get_by_id(db: Session, scraped_price_id: int):
        return db.query(models.ScrapedPrice).filter(models.ScrapedPrice.id == scraped_price_id).first()

    def create(db: Session, scraped_price: schemas.ScrapedPriceCreate):
        db_scraped_price = models.ScrapedPrice(**scraped_price.dict())
        db.add(db_scraped_price)
        db.commit()
        db.refresh(db_scraped_price)
        return db_scraped_price

    def update(db: Session, scraped_price_id: int, scraped_price: schemas.ScrapedPriceUpdate):
        db_scraped_price = db.query(models.ScrapedPrice).filter(models.ScrapedPrice.id == scraped_price_id).first()
        for key, value in scraped_price.dict().items():
            if value is not None:
                setattr(db_scraped_price, key, value)
        db.commit()
        return db_scraped_price

    def delete(db: Session, scraped_price_id: int):
        try:
            db_scraped_price = db.query(models.ScrapedPrice).filter(models.ScrapedPrice.id == scraped_price_id).first()
            if db_scraped_price is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scraped price not found")
            db.delete(db_scraped_price)
            db.commit()
            return {"message": "Scraped price deleted successfully"}
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


class Gender:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Gender).offset(min).limit(max).all()
        return db.query(models.Gender).all()

    def get_by_id(db: Session, gender_id: int):
        return db.query(models.Gender).filter(models.Gender.id == gender_id).first()

    def create(db: Session, gender: schemas.GenderCreate):
        db_gender = models.Gender(**gender.dict())
        db.add(db_gender)
        db.commit()
        db.refresh(db_gender)
        return db_gender

    def update(db: Session, gender_id: int, gender: schemas.GenderUpdate):
        db_gender = db.query(models.Gender).filter(models.Gender.id == gender_id).first()
        for key, value in gender.dict().items():
            if value is not None:
                setattr(db_gender, key, value)
        db.commit()
        return db_gender

    def delete(db: Session, gender_id: int):
        try:
            db_gender = db.query(models.Gender).filter(models.Gender.id == gender_id).first()
            if db_gender is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gender not found")
            db.delete(db_gender)
            db.commit()
            return {"message": "Gender deleted successfully"}
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


class Refill:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Refill).filter(models.Refill.deleted_at == None).offset(min).limit(max).all()
        return db.query(models.Refill).filter(models.Refill.deleted_at == None).all()

    def get_by_id(db: Session, refill_id: int):
        return db.query(models.Refill).filter(models.Refill.id == refill_id, models.Refill.deleted_at == None).first()

    def create(db: Session, refill: schemas.RefillCreate):
        db_refill = models.Refill(**refill.dict())

        agent = db.query(models.Agent).filter(models.Agent.id == refill.agent_id).first()
        agent.balance += refill.amount

        db.add(db_refill)
        db.commit()
        db.refresh(db_refill)
        return db_refill

    def update(db: Session, refill_id: int, refill: schemas.RefillUpdate):
        """ get refill and find difference between old and new amount than add it to agent balance """
        db_refill = db.query(models.Refill, models.Agent). \
            filter(models.Refill.id == refill_id,
                   models.Agent.id == models.Refill.agent_id).first()
        refill_db = db_refill['Refill']
        agent = db_refill['Agent']

        print('before', agent.balance)

        agent.balance += refill.amount - refill_db.amount

        for key, value in refill.dict().items():
            if value is not None:
                setattr(refill_db, key, value)

        db.commit()
        print('after', agent.balance)
        return refill_db

    def delete(db: Session, refill_id: int):
        try:
            refill_db = db.query(models.Refill, models.Agent). \
                filter(models.Refill.id == refill_id,
                       models.Agent.id == models.Refill.agent_id).first()

            db_refill = refill_db['Refill']
            agent = refill_db['Agent']

            if db_refill is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refill not found")
            agent.balance -= db_refill.amount

            if db_refill is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refill not found")

            if db_refill.deleted_at is not None:
                return {"message": "Refill already deleted"}

            db_refill.deleted_at = datetime.now()
            db.commit()
            return {"message": "Refill deleted successfully"}
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# Agent Debt
class AgentDebt:
    # get list of agent debts with agent id
    def get_list(db: Session, agent_id: int, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.AgentDebt).filter(models.AgentDebt.agent_id == agent_id).offset(min).limit(max).all()
        return db.query(models.AgentDebt).filter(models.AgentDebt.agent_id == agent_id).all()