from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime
import traceback
import logging

from pages.views.main import add_time

routers = APIRouter()


def get_tickets_by_flight(db: Session, from_date=None, to_date=None,
                          page=None, limit=None, agent_id: int = None,
                          flight_id: int = None, search_text=None):
    """ get tickets by departure_date is >= now and on_sale <= now """
    try:
        if from_date and to_date:
            from_date, to_date = add_time(from_date, to_date)

        query = f"SELECT t.id, t.created_at, t.ticket_number, \
                        json_build_object( \
                            'id', f.id, \
                            'flight_number', fg.flight_number, \
                            'departure_date', f.departure_date, \
                            'price', f.price, \
                            'currency', f.currency \
                        ) AS flight, \
                        CONCAT(t.first_name, ' ', t.surname) AS passenger, \
                        u.username AS agent, \
                        t.comment, t.is_booked, \
                        json_build_object( \
                            'id', ts.id, \
                            'name_ru', ts.name_ru, \
                            'name_en', ts.name_en, \
                            'name_uz', ts.name_uz \
                        ) AS ticket_status, \
                        COALESCE( \
                            json_build_object( \
                                'id', ad.id, \
                                'amount', ad.amount, \
                                'comment', ad.comment), '[]') AS agent_debt \
                    FROM tickets AS t \
                    JOIN flights AS f ON t.flight_id = f.id \
                    JOIN flight_guides AS fg ON f.flight_guide_id = fg.id \
                    JOIN agents AS a ON t.agent_id = a.id \
                    JOIN users AS u ON a.user_id = u.id \
                    JOIN ticket_statuses AS ts ON t.status_id = ts.id \
                    LEFT JOIN agent_debts AS ad ON t.id = ad.ticket_id \
                    WHERE f.deleted_at IS NULL "

        if from_date and to_date:
            query += f"AND f.departure_date BETWEEN '{from_date}' AND '{to_date}' "
            if from_date and from_date.timestamp() >= datetime.now().timestamp():
                query += f"AND f.on_sale <= '{from_date}' "
        else:
            query += f"AND f.departure_date >= '{datetime.now()}' \
                     AND f.on_sale <= '{datetime.now()}' "

        if agent_id:
            query += f"AND t.agent_id = {agent_id} "

        if flight_id:
            query += f"AND t.flight_id = {flight_id} "

        if search_text:
            search_text = search_text.lower()
            query += f"AND (fg.flight_number::text LIKE '%{search_text}%' \
                          OR LOWER(t.first_name) LIKE '%{search_text}%' \
                            OR LOWER(t.surname) LIKE '%{search_text}%' \
                            OR t.ticket_number::text LIKE '%{search_text}%' \
                            OR LOWER(u.username) LIKE '%{search_text}%' \
                            OR LOWER(t.comment) LIKE '%{search_text}%' \
                            OR LOWER(ts.name_ru) LIKE '%{search_text}%' \
                            OR LOWER(ts.name_en) LIKE '%{search_text}%' \
                            OR LOWER(ts.name_uz) LIKE '%{search_text}%' \
                            OR f.price::text LIKE '%{search_text}%' ) "

        query += f"ORDER BY f.departure_date, t.created_at "

        counter = db.execute(text(query)).fetchall()

        if limit is not None and page is not None:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"
        return db.execute(text(query)).fetchall(), len(counter)

    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))
