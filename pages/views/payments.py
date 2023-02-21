from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime
import traceback
import logging


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
            search_text = search_text.lower()
            query += f"AND (LOWER(r.comment) LIKE '%{search_text}%' \
                            OR LOWER(u.username) LIKE '%{search_text}%' \
                            OR LOWER(a.company_name) LIKE '%{search_text}%') "

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
