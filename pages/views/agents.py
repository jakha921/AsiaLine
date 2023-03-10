from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session
import traceback
import logging

routers = APIRouter()


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

        counter = db.execute(query).fetchall()

        query += f"ORDER BY a.balance "
        if limit and page:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(query).fetchall(), len(counter)
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

        counter = db.execute(query).fetchall()

        query += f"ORDER BY d.amount "
        if page and limit:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(query).fetchall(), len(counter)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))
