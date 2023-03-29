import logging

from sqlalchemy.orm import Session
from datetime import datetime, date

from pages.views.main import add_time


def get_flights_by_range_date(db: Session,
                              from_date: date = None,
                              to_date: date = None,
                              page: int = None,
                              limit: int = None,
                              search_text: str = None,
                              is_on_sale: bool = False):
    """ Get flights by range date """
    if from_date and to_date:
        from_date, to_date = add_time(from_date, to_date)

    query = f"SELECT f.id, f.departure_date, fg.flight_number,  f.price, f.currency,\
                    json_build_object( \
                        'id', a1.id, \
                        'airport_ru', a1.airport_ru, \
                        'airport_en', a1.airport_en, \
                        'airport_uz', a1.airport_uz, \
                        'code', a1.code \
                        ) AS from_airport, \
                    json_build_object( \
                        'id', a2.id, \
                        'airport_ru', a2.airport_ru, \
                        'airport_en', a2.airport_en, \
                        'airport_uz', a2.airport_uz, \
                        'code', a2.code \
                    ) AS to_airport, \
                    f.total_seats, f.left_seats, f.on_sale , \
                    (COALESCE(SUM(b.hard_block) + SUM(b.soft_block), 0)) AS booked_seats, \
                    (SELECT COUNT(*) FROM tickets AS t WHERE t.flight_id = f.id AND t.deleted_at IS NULL) AS tickets_count \
                    FROM flights AS f \
                    JOIN flight_guides AS fg ON f.flight_guide_id = fg.id \
                    JOIN airports AS a1 ON fg.from_airport_id = a1.id \
                    JOIN airports AS a2 ON fg.to_airport_id = a2.id \
                    LEFT JOIN bookings AS b ON f.id = b.flight_id \
                    WHERE f.deleted_at IS NULL "

    if from_date and to_date:
        query += f"AND f.departure_date BETWEEN '{from_date}' AND '{to_date}' "
        if from_date.timestamp() >= datetime.now().timestamp() and not is_on_sale:
            query += f"AND f.on_sale <= '{datetime.now()}' "
        elif from_date.timestamp() >= datetime.now().timestamp() and is_on_sale:
            query += f"AND f.on_sale >= '{datetime.now()}' "
    else:
        query += f"AND f.departure_date >= '{datetime.now()}' "
        if not is_on_sale:
            query += f"AND f.on_sale <= '{datetime.now()}' "
        else:
            query += f"AND f.on_sale >= '{datetime.now()}' "

    if search_text:
        search_text = search_text.lower()
        query += f"AND (LOWER(fg.flight_number) LIKE '%{search_text}%' \
                    OR LOWER(a1.airport_ru) LIKE '%{search_text}%' \
                    OR LOWER(a1.airport_en) LIKE '%{search_text}%' \
                    OR LOWER(a1.airport_uz) LIKE '%{search_text}%' \
                    OR LOWER(a2.airport_ru) LIKE '%{search_text}%' \
                    OR LOWER(a2.airport_en) LIKE '%{search_text}%' \
                    OR LOWER(a2.airport_uz) LIKE '%{search_text}%' \
                    OR f.price::text LIKE '%{search_text}%' \
                    OR f.total_seats::text LIKE '%{search_text}%' \
                    OR f.left_seats::text LIKE '%{search_text}%') "

    query += "GROUP BY f.id, fg.flight_number, a1.id, a2.id "
    query += "ORDER BY f.departure_date "

    counter = db.execute(query).fetchall()

    if page and limit:
        query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

    return db.execute(query).fetchall(), len(counter)


def get_flight_quotes(db, flight_id: int, from_date, to_date,
                      page: int = None, limit: int = None, search_text: str = None):
    """ Get booking by flight_id """
    try:
        if from_date and to_date:
            from_date, to_date = add_time(from_date, to_date)

        query = f"SELECT f.id, fg.flight_number, f.departure_date, f.price, f.currency, f.left_seats, f.total_seats, \
                    json_agg(\
                        json_build_object(\
                            'booking_id', b.id, \
                            'hard_block', b.hard_block, \
                            'soft_block', b.soft_block, \
                            'price', b.price, \
                            'currency', b.currency, \
                            'agent_id', a.id, \
                            'company_name', a.company_name) \
                    ) AS bookings \
                    FROM flights AS f \
                    JOIN flight_guides AS fg ON f.flight_guide_id = fg.id \
                    LEFT JOIN bookings AS b ON f.id = b.flight_id \
                    JOIN agents AS a ON b.agent_id = a.id \
                    WHERE f.deleted_at IS NULL \
                    AND b.deleted_at IS NULL "

        if from_date and to_date:
            query += f"AND f.departure_date BETWEEN '{from_date}' AND '{to_date}' "
        else:
            query += f"AND f.departure_date >= '{datetime.now()}' "

        if flight_id:
            query += f"AND f.id = {flight_id} "

        if search_text and not search_text.isdigit():
            search_text = search_text.lower()
            query += f"AND (fg.flight_number::text LIKE '%{search_text}%' \
                        OR LOWER(a.company_name) LIKE '%{search_text}%' \
                        OR b.price::text LIKE '%{search_text}%' \
                        OR b.hard_block::text LIKE '%{search_text}%' \
                        OR b.soft_block::text LIKE '%{search_text}%') "

        query += f"GROUP BY f.id, fg.flight_number "

        query += f"ORDER BY f.departure_date "

        counter = db.execute(query).fetchall()

        if page and limit:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(query).fetchall(), len(counter)

    except Exception as e:
        print(logging.error(e))
