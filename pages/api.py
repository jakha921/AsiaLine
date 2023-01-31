from fastapi import APIRouter
from sqlalchemy import text
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


def get_flights_by_range_departure_date(db: Session, from_date, to_date, page=None, limit=None, search_text=None,
                                        book: bool = False):
    """ Get flights where now <= departure_date <= now """
    if from_date is not None and to_date is not None:
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
                    f.total_seats, f.left_seats "

    if book:
        query += ", (SUM(b.hard_block) + SUM(b.soft_block)) AS booked_seats, \
                    json_agg(json_build_object( \
                        'id', b.id, \
                        'hard_block', b.hard_block, \
                        'soft_block', b.soft_block, \
                        'agent', a.company_name \
                    )) AS booking "

    query += f"FROM flights AS f \
                JOIN airports AS a1 ON f.from_airport_id = a1.id \
                JOIN airports AS a2 ON f.to_airport_id = a2.id "

    if book:
        query += f"LEFT JOIN bookings AS b ON f.id = b.flight_id \
                   LEFT JOIN agents AS a ON b.agent_id = a.id "

    query += f"WHERE f.deleted_at IS NULL "

    if from_date and to_date:
        query += f"AND f.departure_date BETWEEN '{from_date}' AND '{to_date}' \
               AND f.on_sale <= '{from_date}' "
    else:
        query += f"AND f.departure_date >= '{datetime.now()}' \
               AND f.on_sale <= '{datetime.now()}' "

    if search_text and not search_text.isdigit():
        query += f"AND (f.flight_number LIKE '%{search_text}%' \
                OR a1.airport_ru LIKE '%{search_text}%' \
                OR a1.airport_en LIKE '%{search_text}%' \
                OR a1.airport_uz LIKE '%{search_text}%' \
                OR a2.airport_ru LIKE '%{search_text}%' \
                OR a2.airport_en LIKE '%{search_text}%' \
                OR a2.airport_uz LIKE '%{search_text}%') "

    if search_text and search_text.isdigit():
        query += f"AND (f.price={search_text} \
                OR f.total_seats={search_text} \
                OR f.left_seats={search_text} \
                OR booked_seats={search_text}) "

    if book:
        query += f"GROUP BY f.id, a1.id, a2.id "

    query += f"ORDER BY f.departure_date "
    if page is not None and limit is not None:
        query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

    db_query = db.execute(query).fetchall()
    foo = db_query[4][9]
    for flight in db_query:
        if flight[9] is None:
            foo = list(flight)
            print(flight[0])
            print(flight[9])
            # flight[8] = []
            # flight[10] = []
            flight = tuple(foo)

    return db_query


# region Statics
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


def get_flights_by_on_sale_date_and_search(db: Session, from_date, to_date, page, limit, search_text=None):
    """ get flights by on_sale is >= now """
    try:
        if from_date is not None and to_date is not None:
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
                        f.on_sale, f.total_seats, f.left_seats, \
                        (SUM(b.hard_block) + SUM(b.soft_block)) AS booked_seats \
                    FROM flights AS f \
                    JOIN airports AS a1 ON f.from_airport_id = a1.id \
                    JOIN airports AS a2 ON f.to_airport_id = a2.id \
                    LEFT JOIN bookings AS b ON f.id = b.flight_id \
                    WHERE f.deleted_at IS NULL "

        if from_date and to_date:
            query += f"AND f.departure_date BETWEEN '{from_date}' AND '{to_date}' \
                    AND f.on_sale >= '{from_date}' "
        else:
            query += f"AND f.departure_date >= '{datetime.now()}' \
                    AND f.on_sale >= '{datetime.now()}' "

        if search_text and not search_text.isdigit():
            query += f"AND (f.flight_number LIKE '%{search_text}%' \
                       OR a1.airport_ru LIKE '%{search_text}%' \
                       OR a1.airport_en LIKE '%{search_text}%' \
                       OR a1.airport_uz LIKE '%{search_text}%' \
                       OR a2.airport_ru LIKE '%{search_text}%' \
                       OR a2.airport_en LIKE '%{search_text}%' \
                       OR a2.airport_uz LIKE '%{search_text}%') "

        if search_text and search_text.isdigit():
            query += f"AND (f.price={search_text} \
                       OR f.total_seats={search_text} \
                       OR f.left_seats={search_text} \
                       OR booked_seats={search_text}) "

        query += f"GROUP BY f.id, a1.id, a2.id \
                 ORDER BY f.departure_date "

        if page and limit:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"
        return db.execute(text(query)).fetchall()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_quotas_by_flight_id(db, flight_id: int, from_date, to_date, page: int, limit: int, search_text: str = None,
                            agent_id: int = None):
    """ Get booking by flight_id """
    try:
        if from_date and to_date:
            from_date, to_date = add_time(from_date, to_date)

        query = f"SELECT f.id, f.flight_number, f.departure_date, f.price, f.currency, f.left_seats, \
                    json_build_object('id', a.id, 'name', a.company_name) AS agent, b.hard_block, b.soft_block \
                    FROM flights AS f \
                    JOIN bookings AS b ON f.id = b.flight_id \
                    JOIN agents AS a ON b.agent_id = a.id \
                    WHERE f.deleted_at IS NULL "

        if from_date and to_date:
            query += f"AND f.departure_date BETWEEN '{from_date}' AND '{to_date}' "
        else:
            query += f"AND f.departure_date >= '{datetime.now()}' "

        if flight_id:
            query += f"AND f.id = {flight_id} "

        if agent_id:
            query += f"AND a.id = {agent_id} "

        if search_text and not search_text.isdigit():
            query += f"AND (f.flight_number LIKE '%{search_text}%' \
                       OR a.company_name LIKE '%{search_text}%') "

        if search_text and search_text.isdigit():
            query += f"AND (f.price = {search_text} \
                        OR f.left_seats = {search_text}) "

        query += f"ORDER BY f.departure_date "
        if page and limit:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_tickets_by_departure_date_and_on_sale(db: Session, from_date=None, to_date=None,
                                              page=None, limit=None, agent_id: int = None,
                                              flight_id: int = None, search_text=None):
    """ get tickets by departure_date is >= now and on_sale <= now """
    try:
        if from_date and to_date:
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
                    WHERE f.deleted_at IS NULL "

        if from_date and to_date:
            query += f"AND f.departure_date BETWEEN '{from_date}' AND '{to_date}' \
                   AND f.on_sale <= '{from_date}' "
        else:
            query += f"AND f.departure_date >= '{datetime.now()}' \
                   AND f.on_sale <= '{datetime.now()}' "

        if agent_id:
            query += f"AND t.agent_id = {agent_id} "

        if flight_id:
            query += f"AND t.flight_id = {flight_id} "

        if search_text and not search_text.isdigit():
            query += f"AND (f.flight_number LIKE '%{search_text}%' \
                       OR u.username LIKE '%{search_text}%' \
                       OR f.flight_number LIKE '%{search_text}%' \
                       OR t.ticket_number LIKE '%{search_text}%' \
                       OR t.first_name LIKE '%{search_text}%' \
                       OR u.username LIKE '%{search_text}%' \
                       OR t.surname LIKE '%{search_text}%' ) "

        if search_text and search_text.isdigit():
            query += f"AND f.price = {search_text} "

        query += f"ORDER BY f.departure_date, t.created_at "
        if limit is not None and page is not None:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"
        return db.execute(text(query)).fetchall()

    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


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

        query += f"ORDER BY u.id "
        if limit and page:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

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
def get_refill_by_agent_id(db: Session, from_date, to_date, agent_id=None, page=None, limit=None, search_text=None):
    """ get tickets by departure_date is >= now and on_sale <= now """
    try:
        if from_date and to_date:
            from_date, to_date = add_time(from_date, to_date)

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
        else:
            query += f"AND r.created_at <= '{datetime.now()}' "

        if agent_id:
            query += f"AND r.agent_id = {agent_id} "

        if search_text and not search_text.isdigit():
            query += f"AND (r.comment LIKE '%{search_text}%' \
                            OR u.username LIKE '%{search_text}%' \
                            OR a.company_name LIKE '%{search_text}%') "

        if search_text and search_text.isdigit():
            query += f"AND (r.amount = {search_text}) "

        query += f"ORDER BY r.created_at "
        if limit and page:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_agents_balance(db: Session, agent_id, page: int = None, limit: int = None):
    """ get agents by agent_id if agent_id is None then get all agents """
    try:
        query = f"SELECT agents.id, agents.company_name, agents.balance \
                FROM agents \
                WHERE agents.deleted_at IS NULL "

        if agent_id:
            query += f"AND agents.id = agent_id "

        query += f"ORDER BY agents.balance "
        if limit and page:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_agents_discounts(db: Session, agent_id, page: int, limit: int, searching_text: str = None):
    """ get agents and discounts by agent_id """
    try:
        query = f"SELECT a.id, a.company_name, u.email, \
                json_build_object('amount', d.amount, 'name', d.name) AS discount, \
                a.balance, a.is_on_credit \
                FROM agents AS a \
                JOIN users AS u ON a.user_id = u.id \
                JOIN discounts AS d ON a.discount_id = d.id \
                WHERE a.deleted_at IS NULL "

        if agent_id:
            query += f"AND a.id = {agent_id} "

        if searching_text and not searching_text.isdigit():
            query += f"AND (a.company_name LIKE '%{searching_text}%' \
                        OR u.email LIKE '%{searching_text}%' \
                        OR d.name LIKE '%{searching_text}%') "

        if searching_text and searching_text.isdigit():
            query += f"AND d.amount = {searching_text} "

        query += f"ORDER BY a.balance "
        if limit and page:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_discounts(db: Session, searching_text, page: int, limit: int):
    """ get discounts """
    try:
        query = f"SELECT d.id, d.name, d.amount \
                FROM discounts AS d "

        if searching_text and not searching_text.isdigit():
            query += f"WHERE d.name LIKE '%{searching_text}%' "

        if searching_text and searching_text.isdigit():
            query += f"WHERE d.amount = {searching_text} "

        query += f"ORDER BY d.amount "
        if page and limit:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_guiede(db: Session, searching_text: str, page: int, limit: int):
    """ get airports """
    try:
        query = f"WITH cte AS ( \
                  SELECT cn.country_ru AS country_ru, \
                         cn.country_en AS country_en, \
                         cn.country_uz AS country_uz, \
                         ct.id AS city_id, \
                         ct.city_ru AS city_ru, \
                         ct.city_en AS city_en, \
                         ct.city_uz AS city_uz, \
                         a.id AS airport_id, \
                         a.airport_ru AS airport_ru, \
                         a.airport_en AS airport_en, \
                         a.airport_uz AS airport_uz, \
                  FROM countries c \
                  LEFT JOIN cities ci ON c.id = ci.country_id \
                  LEFT JOIN airports a ON ci.id = a.city_id) \
                  SELECT cn.id, cn.country_ru, cn.country_en, cn.country_ru, \
                      json_agg(json_build_object( \
                        'id', ct.id, \
                        'city_ru', ct.city_ru, \
                        'city_en', ct.city_en, \
                        'city_uz', ct.city_uz \
                      json_agg(json_build_object( \
                            'id', a.id, \
                            'airport_ru', a.airport_ru, \
                            'airport_en', a.airport_en, \
                            'airport_uz', a.airport_uz)))) AS cities \
                  FROM cte AS cn \
                  LEFT JOIN cities AS ct ON cn.id = ct.country_id \
                  LEFT JOIN airports AS a ON ct.id = a.city_id "

        if searching_text:
            query += f"AND (cn.country_ru LIKE '%{searching_text}%', \
                    OR cn.country_en LIKE '%{searching_text}%', \
                    OR cn.country_uz LIKE '%{searching_text}%', \
                    OR ct.city_ru LIKE '%{searching_text}%', \
                    OR ct.city_en LIKE '%{searching_text}%', \
                    OR ct.city_uz LIKE '%{searching_text}%', \
                    OR a.airport_ru LIKE '%{searching_text}%', \
                    OR a.airport_en LIKE '%{searching_text}%', \
                    OR a.airport_uz LIKE '%{searching_text}%') "

        query += f"GROUP by cn.id \
                 ORDER BY cn.country_ru"
        if page and limit:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall()
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
