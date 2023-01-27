from fastapi import APIRouter
from sqlalchemy import func, case, text
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import traceback
import logging

from users.currency_rate import get_currency_rate
from db import models

routers = APIRouter()


def add_time(from_date, to_date):
    """ To exist date add min and max time """
    from_date = datetime.combine(from_date, datetime.now().time())
    to_date = datetime.combine(to_date, datetime.max.time())
    return from_date, to_date


def update_currency_rate(db: Session):
    """ get currency rate from api and update currency rate """
    currency_rate = get_currency_rate()
    print(currency_rate)
    db_currency_rate = models.CurrencyRate(
        rub_to_usd=currency_rate['RUBUSD'],
        rub_to_eur=currency_rate['RUBEUR'],
        rub_to_uzs=currency_rate['RUBUZS'],
        updated_at=currency_rate['updated_at']
    )
    db.add(db_currency_rate)
    db.commit()
    db.refresh(db_currency_rate)
    return db_currency_rate


def get_currency_last_item(db: Session):
    """ Get last currency rate if updated_at <= 24 hours, update currency rate """
    db_currency_rate = db.query(models.CurrencyRate).order_by(models.CurrencyRate.updated_at.desc()).first()
    if not db_currency_rate:
        update_currency_rate(db)
        get_currency_last_item(db)
    if db_currency_rate.updated_at <= datetime.now() - timedelta(hours=24):
        db_currency_rate = update_currency_rate(db)

    return db_currency_rate


# Statics
def get_flights_by_range_departure_date(db: Session, from_date, to_date, page=None, limit=None, search_text=None):
    """ Get flights where now <= departure_date <= now """
    from_date, to_date = add_time(from_date, to_date)

    query = f"SELECT f.id, f.flight_number, f.departure_date, f.price, f.currency, \
                    json_build_object( \
                        'id', a1.id, \
                        'airport_ru', a1.airport_ru, \
                        'airport_en', a1.airport_en, \
                        'airport_uz', a1.airport_uz \
                        ) AS from_airport, \
                    json_build_object( \
                        'id', a2.id, \
                        'airport_ru', a2.airport_ru, \
                        'airport_en', a2.airport_en, \
                        'airport_uz', a2.airport_uz \
                    ) AS to_airport, \
                    f.total_seats, f.left_seats \
                FROM flights AS f \
                JOIN airports AS a1 ON f.from_airport_id = a1.id \
                JOIN airports AS a2 ON f.to_airport_id = a2.id \
                WHERE f.deleted_at IS NULL \
                AND f.departure_date BETWEEN '{from_date}' AND '{to_date}' \
                AND f.on_sale <= '{from_date}' "

    if search_text and not search_text.isdigit():
        query += f"AND (f.flight_number LIKE '%{search_text}%' \
                OR a1.airport_ru LIKE '%{search_text}%' \
                OR a1.airport_en LIKE '%{search_text}%' \
                OR a1.airport_uz LIKE '%{search_text}%' \
                OR a2.airport_ru LIKE '%{search_text}%' \
                OR a2.airport_en LIKE '%{search_text}%' \
                OR a2.airport_uz LIKE '%{search_text}%') "

    if search_text is not None and search_text.isdigit():
        # search_text = int(search_text)
        # print(type(search_text))
        query += f"AND (f.price LIKE '%{search_text}%' \
                   OR f.left_seats LIKE '%{search_text}%' \
                   OR f.total_seats LIKE '%{search_text}%') "
    if page is not None and limit is not None:
        query += f"ORDER BY f.departure_date \
                LIMIT {limit} OFFSET {limit * (page - 1)}"

    return db.execute(query).fetchall()


def get_reg_passenger_for_last_30_days(db: Session):
    """ Get registered passenger for last 30 days """
    return db.query(models.Passenger).filter(models.Passenger.created_at >= datetime.now() - timedelta(days=30)).count()


# ! check it status_id
def get_sold_tickets_for_last_30_days(db: Session):
    """ Get sold tickets for last 30 days """
    try:
        return db.query(
            models.Ticket
        ).filter(
            models.Ticket.status_id == 3).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_tickets_by_flight_id(db: Session, flight_id):
    """ Get all tickets by flight_id """
    try:
        return db.query(
            models.Ticket
        ).filter(
            models.Ticket.deleted_at == None,
            models.Ticket.flight_id == flight_id,
            models.Flight.id == models.Ticket.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()
        ).order_by(models.Ticket.created_at, models.Flight.departure_date).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_flights_by_on_sale_date_and_search(db: Session, from_date, to_date, page, limit, search_text=None):
    """ get flights by on_sale is >= now """
    from_date, to_date = add_time(from_date, to_date)

    query = f"SELECT f.id, f.flight_number, f.departure_date, f.price, f.currency, \
                    json_build_object( \
                        'id', a1.id, \
                        'airport_ru', a1.airport_ru, \
                        'airport_en', a1.airport_en, \
                        'airport_uz', a1.airport_uz \
                        ) AS from_airport, \
                    json_build_object( \
                        'id', a2.id, \
                        'airport_ru', a2.airport_ru, \
                        'airport_en', a2.airport_en, \
                        'airport_uz', a2.airport_uz \
                    ) AS to_airport, \
                    f.on_sale, f.total_seats, f.left_seats \
                FROM flights AS f \
                JOIN airports AS a1 ON f.from_airport_id = a1.id \
                JOIN airports AS a2 ON f.to_airport_id = a2.id \
                WHERE f.deleted_at IS NULL \
                AND f.departure_date BETWEEN '{from_date}' AND '{to_date}' \
                AND f.on_sale >= '{from_date}'" \

    if search_text is not None:
        query += f"AND (f.flight_number LIKE '%{search_text}%' \
                   OR a1.airport_ru LIKE '%{search_text}%' \
                   OR a1.airport_en LIKE '%{search_text}%' \
                   OR a1.airport_uz LIKE '%{search_text}%' \
                   OR a2.airport_ru LIKE '%{search_text}%' \
                   OR a2.airport_en LIKE '%{search_text}%' \
                   OR a2.airport_uz LIKE '%{search_text}%') "
        # OR f.price LIKE '%{search_text}%' \
        # OR f.left_seats LIKE '%{search_text}%' \

    query += f"ORDER BY f.departure_date \
                LIMIT {limit} OFFSET {limit * (page - 1)}"
    return db.execute(text(query)).fetchall()


def get_quotas_by_flight_id(db, from_date, to_date, page, limit, search_text=None):
    """ Get booking by flight_id """
    try:
        from_date, to_date = add_time(from_date, to_date)

        query = f"SELECT f.id, f.flight_number, f.departure_date, f.price, f.currency, f.left_seats, \
                    u.username, b.hard_block, b.soft_block \
                    FROM flights AS f \
                    JOIN bookings AS b ON f.id = b.flight_id \
                    JOIN agents AS a ON b.agent_id = a.id \
                    JOIN users AS u ON a.user_id = u.id \
                    WHERE f.deleted_at IS NULL \
                    AND f.departure_date BETWEEN '{from_date}' AND '{to_date}' \
                    AND f.on_sale <= '{from_date}'"

        if search_text is not None:
            query += f"AND (f.flight_number LIKE '%{search_text}%' \
                       OR u.username LIKE '%{search_text}%') "

        query += f"ORDER BY f.departure_date \
                    LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_tickets_by_departure_date_and_on_sale(db: Session, from_date, to_date, page, limit,
                                              agent_id: int = None, flight_id: int = None, search_text=None):
    """ get tickets by departure_date is >= now and on_sale <= now """
    # try:
    from_date, to_date = add_time(from_date, to_date)

    query = f"SELECT t.id, t.created_at, t.ticket_number, \
                    json_build_object( \
                        'id', f.id, \
                        'flight_number', f.flight_number, \
                        'departure_date', f.departure_date, \
                        'price', f.price, \
                        'currency', f.currency \
                    ) AS flight, \
                    CONCAT(t.first_name, t.surname) AS passenger, \
                    u.username AS agent, \
                    t.comment  \
                FROM tickets AS t \
                JOIN flights AS f ON t.flight_id = f.id \
                JOIN agents AS a ON t.agent_id = a.id \
                JOIN users AS u ON a.user_id = u.id \
                WHERE f.deleted_at IS NULL \
                AND f.departure_date BETWEEN '{from_date}' AND '{to_date}' \
                AND f.on_sale <= '{from_date}'"

    if agent_id:
        query += f"AND t.agent_id = {agent_id} "

    if flight_id:
        query += f"AND t.flight_id = {flight_id} "

    if search_text is not None:
        query += f"AND (f.flight_number LIKE '%{search_text}%' \
                   OR u.username LIKE '%{search_text}%' \
                   OR t.ticket_number LIKE '%{search_text}%' \
                   OR t.first_name LIKE '%{search_text}%' \
                   OR t.surname LIKE '%{search_text}%' ) "

    if limit is not None and page is not None:
        query += f"ORDER BY f.departure_date, t.created_at \
                LIMIT {limit} OFFSET {limit * (page - 1)}"
    return db.execute(text(query)).fetchall()

    # except Exception as e:
    #     print(logging.error(traceback.format_exc()))
    #     print(logging.error(e))


def get_all_users_with_role(db: Session, page: int, limit: int, search_text=None):
    """ get all passengers with role """
    try:
        query = f"SELECT u.id, u.username, u.email, \
                    json_build_object( \
                        'id', r.id, \
                        'title_ru', r.title_ru, \
                        'title_en', r.title_en, \
                        'title_uz', r.title_uz \
                    ) AS role \
                FROM users AS u \
                JOIN roles AS r ON u.role_id = r.id \
                WHERE u.deleted_at IS NULL "

        if search_text is not None:
            query += f"AND (u.username LIKE '%{search_text}%' \
                          OR u.email LIKE '%{search_text}%' \
                            OR r.title_ru LIKE '%{search_text}%' \
                            OR r.title_en LIKE '%{search_text}%' \
                            OR r.title_uz LIKE '%{search_text}%') "

        if limit is not None and page is not None:
            query += f"ORDER BY u.id \
                    LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_all_roles(db: Session, page: int, limit: int, search_text=None):
    """ get all roles """
    try:
        query = f"SELECT r.id, r.title_ru, r.title_en, r.title_uz \
                FROM roles AS r "
                # LEFT JOIN role_permissions AS rp ON r.id = rp.role_id \
                # LEFT JOIN permissions AS p ON rp.permission_id = p.id \
                # LEFT JOIN sections AS s ON p.section_id = s.id "

        if search_text is not None:
            query += f"WHERE r.title_ru LIKE '%{search_text}%' \
                            OR r.title_en LIKE '%{search_text}%' \
                            OR r.title_uz LIKE '%{search_text}%' "

        if limit is not None and page is not None:
            query += f"ORDER BY r.id \
                    LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


# get tickets by agent_id
def get_tickets_by_agent_id(db: Session, from_date, to_date, agent_id=None, page=None, limit=None, search_text=None):
    """ get tickets by departure_date is >= now and on_sale <= now """
    try:
        from_date, to_date = add_time(from_date, to_date)
        # if agent_id:
        #     return db.query(
        #         models.Refill, models.Agent, models.User
        #     ).filter(
        #         models.Refill.deleted_at == None,
        #         models.Refill.created_at >= from_date,
        #         models.Refill.created_at <= to_date,
        #         models.Refill.agent_id == agent_id,
        #         models.Agent.id == models.Refill.agent_id,
        #         models.User.id == models.Refill.receiver_id
        #     ).order_by(models.Refill.created_at).all()
        #
        # return db.query(
        #     models.Refill, models.Agent, models.User
        # ).filter(
        #     models.Refill.deleted_at == None,
        #     models.Refill.created_at >= from_date,
        #     models.Refill.created_at <= to_date,
        #     models.Agent.id == models.Refill.agent_id,
        #     models.User.id == models.Refill.receiver_id,
        # ).order_by(models.Refill.created_at.desc()).all()
        query = f"SELECT r.id, r.created_at, r.amount, r.comment, \
                    json_build_object( \
                        'id', a.id, \
                        'username', a.company_name \
                    ) AS agent, \
                    json_build_object( \
                        'id', u.id, \
                        'username', u.username \
                    ) AS receiver \
                FROM refills AS r \
                JOIN agents AS a ON r.agent_id = a.id \
                JOIN users AS u ON r.receiver_id = u.id \
                WHERE r.deleted_at IS NULL "

        if from_date and to_date:
            query += f"AND r.created_at BETWEEN '{from_date}' AND '{to_date}' "

        if agent_id:
            query += f"AND r.agent_id = {agent_id} "

        if search_text is not None:
            query += f"AND (r.amount LIKE '%{search_text}%' \
                            OR r.comment LIKE '%{search_text}%' \
                            OR u.username LIKE '%{search_text}%' \
                            OR a.company_name LIKE '%{search_text}%') "

        if limit is not None and page is not None:
            query += f"ORDER BY r.created_at \
                    LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_agents_balance(db: Session, agent_id):
    """ get agents by agent_id if agent_id is None then get all agents """
    try:
        if agent_id:
            return db.query(
                models.Agent
            ).filter(
                models.Agent.id == agent_id,
                models.Agent.deleted_at == None
            ).all()
        else:
            return db.query(
                models.Agent
            ).filter(
                models.Agent.deleted_at == None
            ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_agents_discounts(db: Session, agent_id):
    """ get agents and discounts by agent_id """
    try:
        if agent_id:
            return db.query(
                models.Agent, models.Discount
            ).filter(
                models.Agent.id == agent_id,
                models.Agent.discount_id == models.Discount.id,
                models.Agent.deleted_at == None,
                models.User.id == models.Agent.user_id
            ).all()

        return db.query(
            models.Agent, models.Discount, models.User
        ).filter(
            models.Agent.discount_id == models.Discount.id,
            models.Agent.deleted_at == None,
            models.User.id == models.Agent.user_id
        ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_discounts(db: Session):
    """ get discounts """
    try:
        return db.query(
            models.Discount
        ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_airports(db: Session):
    """ get airports """
    try:
        return db.query(
            models.Airport
        ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_cities(db: Session):
    """ get cities """
    try:
        return db.query(
            models.City
        ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_countries(db: Session):
    """ get countries """
    try:
        return db.query(
            models.Country
        ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_ticket_classes(db: Session):
    """ get ticket class """
    try:
        return db.query(
            models.TicketClass
        ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))
