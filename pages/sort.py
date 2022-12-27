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


def sort_flights(db, flights, lang='ru') -> list:
    if lang == "en":
        lang = "en"
    elif lang == "uz":
        lang = "uz"
    else:
        lang = "ru"

    # add to end
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
                "id": from_airport.get("id"),
                "airport": from_airport.get(f"airport_{lang}") if from_airport.get(f"airport_{lang}") else None,
                "short_name": from_airport.get("short_name") if from_airport.get("short_name") else None,
                "city": from_airport["city"][f"city_{lang}"] if from_airport["city"][f"city_{lang}"] else None,
            },
            "to_airport": {
                "id": to_airport.get("id"),
                "airport": to_airport.get(f"airport_{lang}") if to_airport.get(f"airport_{lang}") else None,
                "short_name": to_airport.get("short_name") if to_airport.get("short_name") else None,
                "city": to_airport["city"][f"city_{lang}"] if to_airport["city"][f"city_{lang}"] else None,
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


# check it do not used
def sort_booking_add_into_sorted_flights(quotes):
    """ quotes["Booking"].flight_id == quotes["Flight"].id add booking into sorted_flights """
    sorted_flights = []
    for quote in quotes:
        flight = quote["Flight"]
        booking = quote["Booking"]
        from_airport = quote["Flight"].from_airport
        to_airport = quote["Flight"].to_airport
        flight_dict = {
            "id": flight.id,
            "flight_number": flight.flight_number,
            "departure_date": flight.departure_date.strftime("%Y-%m-%d %H:%M:%S"),
            "arrival_date": flight.arrival_date.strftime("%Y-%m-%d %H:%M:%S"),
            "price": flight.price,
            "currency": flight.currency,
            "from_airport": flight.from_airport_id,
            "to_airport": flight.to_airport_id,
            "total_seats": flight.total_seats,
            "left_seats": flight.left_seats,
            "on_sale": flight.on_sale,
            "actor": flight.actor_id,
            "created_at": flight.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": flight.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            # "deleted_at": flight.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if flight.deleted_at else None,
            "booking": {
                "id": booking.id,
                "flight_id": booking.flight_id,
                "agent_id": booking.agent_id,
                "actor_id": booking.actor_id,
                "is_hard_blocked": booking.is_hard_block,
                "sets_count": booking.sets_count,
                "price": booking.price,
                "currency": booking.currency,
            }
        }

        sorted_flights.append(flight_dict)

    return sorted_flights


def sort_tickets(tickets, lang='ru') -> list:
    """ flight_id, agent_id, quota """
    try:
        if lang == "en":
            lang = "en"
        elif lang == "uz":
            lang = "uz"
        else:
            lang = "ru"

        # add to end
        sorted_tickets = []
        for tick in tickets:
            flight = tick['Flight']
            ticket = tick['Ticket']

            ticket_dict = {
                "id": ticket.id,
                "ticket_number": "?",
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
            }

            sorted_passengers.append(passenger_dict)

        return sorted_passengers

    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def sorted_payments(payments):
    try:
        sort_payments = []
        for pay in payments:
            ticket = pay['Ticket']
            transaction = pay['Transaction']
            payment_system = pay['PaymentSystem']

            payment_dict = {
                "id": ticket.id,
                "ticket_created_at": ticket.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "agent_id": ticket.agent_id,
                "full_name": f"{ticket.surname} {ticket.first_name} {ticket.middle_name}" if ticket.middle_name else f"{ticket.surname} {ticket.first_name}",
                "is_online_payment": transaction.is_online_payment,
                "payment_system": {
                    "id": payment_system.id,
                    "name": payment_system.name,
                    "icon": payment_system.icon,
                    "is_active": payment_system.is_active,
                },
                "price": ticket.price,
                "currency": ticket.currency,
                "comment": ticket.comment
            }

            sort_payments.append(payment_dict)

        return sort_payments

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

            agent_dict = {
                "id": agent.id,
                "name": agent.company_name,
                "discount": {
                    "id": discount.id,
                    "formula": discount.amount,
                    "description": discount.name,
                }
            }

            sort_agents.append(agent_dict)

        return sort_agents

    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


if __name__ == "__main__":
    pass
