from pages import api
from users import crud as user_crud
from crud_models import crud

import traceback
import logging


def sort_currency_rate(currency_rate):
    dict_currency_rate = {
        "RUBUSD": currency_rate.rub_to_usd,
        "RUBEUR": currency_rate.rub_to_eur,
        "RUBUZS": currency_rate.rub_to_uzs,
        "updated_at": currency_rate.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    }

    return dict_currency_rate


def sort_by_date_flights(flights):
    # count flights by same date
    flight_by_date = {}
    for flight in flights:
        flight.departure_date = flight.departure_date.date()
        if flight.departure_date in flight_by_date:
            flight_by_date[flight.departure_date] += 1
        else:
            flight_by_date[flight.departure_date] = 1

    # sort dict by date
    flight_by_date = dict(sorted(flight_by_date.items(), key=lambda item: item[0]))
    return flight_by_date


def sort_airport(db, airport_id):
    airport = crud.Airport.get_by_id(db, airport_id)

    airport_dict = {
        "id": airport.id,
        "airport_ru": airport.airport_ru,
        "airport_en": airport.airport_en,
        "airport_uz": airport.airport_uz,
        "city": {
            "id": airport.city_id,
            "city_ru": airport.city.city_ru,
            "city_en": airport.city.city_en,
            "city_uz": airport.city.city_uz,
            "country": {
                "id": airport.city.country_id,
                "country_ru": airport.city.country.country_ru,
                "country_en": airport.city.country.country_en,
                "country_uz": airport.city.country.country_uz,
            }
        }
    }

    return airport_dict


def sort_flights(db, flights) -> list:
    sorted_flights = []
    for flight in flights:
        from_airport = sort_airport(db, flight.from_airport_id)
        to_airport = sort_airport(db, flight.to_airport_id)
        flight_dict = {
            "id": flight.id,
            "flight_number": flight.flight_number,
            "departure_date": flight.departure_date.strftime("%Y-%m-%d %H:%M:%S"),
            "arrival_date": flight.arrival_date.strftime("%Y-%m-%d %H:%M:%S"),
            "price": flight.price,
            "currency": flight.currency,
            "from_airport": {
                "id": from_airport["id"],
                "airport_ru": from_airport["airport_ru"],
                "airport_en": from_airport["airport_en"],
                "airport_uz": from_airport["airport_uz"],
                "city_ru": from_airport["city"][f"city_ru"],
                "city_en": from_airport["city"][f"city_en"],
                "city_uz": from_airport["city"][f"city_uz"],
                "short_name": from_airport.get("short_name") if from_airport.get("short_name") else None,
            },
            "to_airport": {
                "id": to_airport.get("id"),
                "airport_ru": to_airport["airport_ru"],
                "airport_en": to_airport["airport_en"],
                "airport_uz": to_airport["airport_uz"],
                "city_ru": to_airport["city"][f"city_ru"],
                "city_en": to_airport["city"][f"city_en"],
                "city_uz": to_airport["city"][f"city_uz"],
                "short_name": to_airport.get("short_name") if to_airport.get("short_name") else None,
            },
            "total_seats": flight.total_seats,
            "left_seats": flight.left_seats,
            "on_sale": flight.on_sale,
            "actor": flight.actor_id,
            "created_at": flight.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": flight.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            # "deleted_at": flight.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if flight.deleted_at else None,
        }

        sorted_flights.append(flight_dict)

    return sorted_flights


def sort_flight_quotas(flight_quotas) -> list:
    sorted_flight_quotas = []
    for flight_quota in flight_quotas:
        agent = flight_quota['Agent']
        flight = flight_quota['Flight']
        booking = flight_quota['Booking']

        quotas = {
            "id": flight.id,
            "flight_number": flight.flight_number,
            "departure_date": flight.departure_date.strftime("%Y-%m-%d %H:%M:%S"),
            "arrival_date": flight.arrival_date.strftime("%Y-%m-%d %H:%M:%S"),
            "price": flight.price,
            "currency": flight.currency,
            "total_seats": flight.total_seats,
            "left_seats": flight.left_seats,
            "agent": agent.company_name,
            "booking": {
                "id": booking.id,
                "hard_block": booking.hard_block,
                "soft_block": booking.soft_block,
                "price": booking.price,
                "currency": booking.currency,
                "created_at": booking.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": booking.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            },
        }
        sorted_flight_quotas.append(quotas)
    return sorted_flight_quotas


def sort_tickets(tickets) -> list:
    """ flight_id, agent_id, quota """
    try:
        sorted_tickets = []
        for tick in tickets:
            flight = tick['Flight']
            ticket = tick['Ticket']

            ticket_dict = {
                'agent_id': ticket.agent_id,
                "id": ticket.id,
                "ticket_number": ticket.ticket_number,
                "price": ticket.price,
                "currency": ticket.currency,
                'surname': ticket.surname,
                "first_name": ticket.first_name,
                "middle_name": ticket.middle_name,
                "flight": {
                    "id": flight.id,
                    "flight_number": flight.flight_number,
                    "departure_date": flight.departure_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "arrival_date": flight.arrival_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "from_airport": flight.from_airport_id,
                    "to_airport": flight.to_airport_id,
                    "price": flight.price,
                    "currency": flight.currency,
                    "total_seats": flight.total_seats,
                    "left_seats": flight.left_seats,
                },
                "comment": ticket.comment,
                "status": tick["TicketStatus"].name_ru,
                "actor": ticket.actor_id,
                "created_at": ticket.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": ticket.updated_at.strftime("%Y-%m-%d %H:%M:%S") if ticket.updated_at else None,
            }

            sorted_tickets.append(ticket_dict)

        return sorted_tickets


    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def sort_users(passengers) -> list:
    """ ticket_id, agent_id, quota """
    try:
        sorted_passengers = []
        for pas in passengers:
            role = pas['Role']
            passenger = pas['User']

            passenger_dict = {
                "id": passenger.id,
                "email": passenger.email,
                "username": passenger.username,
                "date_joined": passenger.date_joined,
                "role": role.name,
                "role_ru": role.title_ru,
                "role_en": role.title_en,
                "role_uz": role.title_uz,
            }

            sorted_passengers.append(passenger_dict)

        return sorted_passengers

    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def sorted_payments(payments):
    try:
        sorted_payments = []
        for pay in payments:
            refill = pay['Refill']
            agent = pay['Agent']
            user = pay['User']

            payment_dict = {
                "id": refill.id,
                "created_at": refill.created_at.strftime("%Y-%m-%d %H:%M"),
                "agent_id": agent.id,
                "agent": agent.company_name,
                "user_id": user.id,
                "user": user.username,
                "amount": refill.amount,
                "comment": refill.comment
            }
            sorted_payments.append(payment_dict)
        return sorted_payments

    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def sorted_agents(agents):
    """ id, fullname, discount """
    try:
        sort_agents = []
        for agen in agents:
            agent = agen['Agent']
            discount = agen['Discount']
            user = agen['User']

            agent_dict = {
                "id": agent.id,
                "name": agent.company_name,
                "login": user.email,
                "discount": discount.amount,
                "discount_name": discount.name,
                "balance": agent.balance,
                "is_on_credit": agent.is_on_credit,
            }
            sort_agents.append(agent_dict)
        return sort_agents
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


if __name__ == "__main__":
    pass
