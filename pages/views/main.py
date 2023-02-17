import logging
from datetime import date, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db import models


def add_time(from_date, to_date):
    """ To exist date add min and max time """
    if from_date == datetime.now().date():
        from_date = datetime.combine(from_date, datetime.now().time())
    else:
        from_date = datetime.combine(from_date, datetime.min.time())
    to_date = datetime.combine(to_date, datetime.max.time())
    return from_date, to_date


def get_dates_range(db: Session, from_date: date, to_date: date):
    """ Get dates range """
    from_date, to_date = add_time(from_date, to_date)
    return db.query(models.Flight.departure_date).filter(
        models.Flight.deleted_at.is_(None),
        models.Flight.on_sale < from_date,
        models.Flight.departure_date.between(from_date, to_date)).all()


def get_flights_and_search(db: Session, searching_text: str, from_date: date, to_date: date, page: int, limit: int):
    """ Get flights where departure date is between from_date and to_date and search by text """
    try:
        query = f"SELECT f.id, fg.flight_number, f.departure_date, f.price, f.currency, \
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
                f.total_seats, f.left_seats \
                FROM flights AS f \
                JOIN flight_guides AS fg ON f.flight_guide_id = fg.id \
                JOIN airports AS a1 ON fg.from_airport_id = a1.id \
                JOIN airports AS a2 ON fg.to_airport_id = a2.id \
                WHERE f.deleted_at IS NULL "

        if from_date and to_date:
            from_date, to_date = add_time(from_date, to_date)
            query += f"AND f.on_sale < '{from_date}' \
                    AND f.departure_date BETWEEN '{from_date}' AND '{to_date}' "
        else:
            query += f"AND f.on_sale < '{datetime.now()}' \
                    AND f.departure_date > '{datetime.now()}' "

        if searching_text:
            searching_text = searching_text.lower()
            query += f"AND (LOWER(fg.flight_number) LIKE '%{searching_text}%' \
                    OR LOWER(a1.airport_ru) LIKE '%{searching_text}%' \
                    OR LOWER(a1.airport_en) LIKE '%{searching_text}%' \
                    OR LOWER(a1.airport_uz) LIKE '%{searching_text}%' \
                    OR LOWER(a2.airport_ru) LIKE '%{searching_text}%' \
                    OR LOWER(a2.airport_en) LIKE '%{searching_text}%' \
                    OR LOWER(a2.airport_uz) LIKE '%{searching_text}%' \
                    OR f.price::text LIKE '%{searching_text}%' \
                    OR fg.flight_number::text LIKE '%{searching_text}%') "

        query += f"ORDER BY f.departure_date "

        length = len(db.execute(query).fetchall())

        if page and limit:
            query += f"LIMIT {limit} OFFSET {(page - 1) * limit}"

        return db.execute(query).fetchall(), length
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

