from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Session
import traceback
import logging

from pages.views.main import add_time


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

        counter = db.execute(query).fetchall()

        query += f"ORDER BY u.id "
        if limit and page:
            query += f"LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall(), len(counter)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_all_roles(db: Session, page: int, limit: int, search_text=None):
    """ get all roles """
    try:
        query = f"SELECT r.*, COUNT(rp.id) AS permissions_count,\
                COALESCE(json_agg(\
                    jsonb_build_object(\
                        'id', p.id,\
                        'alias', p.alias, \
                        'title_ru', p.title_ru, \
                        'title_en', p.title_en, \
                        'title_uz', p.title_uz, \
                        'descriptions', p.description)) FILTER (WHERE p.id IS NOT NULL), '[]') AS permissions \
                FROM roles AS r \
                LEFT JOIN role_permissions rp ON r.id = rp.role_id \
                LEFT JOIN permissions p ON rp.permission_id = p.id \
                WHERE r.id IS NOT NULL \
                GROUP BY r.id "

        if search_text is not None:
            search_text = search_text.lower()
            query += f"WHERE (LOWER(r.title_ru) LIKE '%{search_text}%' \
                            OR LOWER(r.title_en) LIKE '%{search_text}%' \
                            OR LOWER(r.title_uz) LIKE '%{search_text}%' \
                            OR LOWER(p.title_ru) LIKE '%{search_text}%' \
                            OR LOWER(p.title_en) LIKE '%{search_text}%' \
                            OR LOWER(p.title_uz) LIKE '%{search_text}%' \
                            OR LOWER(p.alias) LIKE '%{search_text}%') "


        counter = db.execute(query).fetchall()

        if limit is not None and page is not None:
            query += f"ORDER BY r.id \
                    LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall(), len(counter)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_all_history(db: Session, page: int, limit: int, search_text=None, user_id=None, from_date=None, to_date=None):
    """ get all history """
    try:
        query = f"SELECT h.id, h.action, h.extra_info, h.created_at, \
                    json_build_object( \
                        'id', u.id, \
                        'username', u.username, \
                        'email', u.email \
                    ) AS user \
                FROM user_history AS h \
                JOIN users AS u ON h.user_id = u.id "

        if search_text is not None:
            search_text = search_text.lower()
            query += f"WHERE (LOWER(h.extra_info) LIKE '%{search_text}%' \
                            OR LOWER(u.username) LIKE '%{search_text}%' \
                            OR LOWER(u.email) LIKE '%{search_text}%') "

        if user_id is not None:
            query += f"AND h.user_id = {user_id} "

        if from_date and to_date:
            query += f"AND h.created_at BETWEEN '{datetime.combine(from_date, datetime.min.time())}' \
                        AND '{datetime.combine(to_date, datetime.max.time())}' "

        counter = db.execute(query).fetchall()

        if limit is not None and page is not None:
            query += f"ORDER BY h.id \
                    LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall(), len(counter)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))
