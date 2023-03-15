from sqlalchemy import text
from sqlalchemy.orm import Session
import traceback
import logging


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
        query = f"SELECT r.id, r.title_ru, r.title_en, r.title_uz \
                FROM roles AS r "

        if search_text is not None:
            query += f"WHERE r.title_ru LIKE '%{search_text}%' \
                            OR r.title_en LIKE '%{search_text}%' \
                            OR r.title_uz LIKE '%{search_text}%' "

        counter = db.execute(query).fetchall()

        if limit is not None and page is not None:
            query += f"ORDER BY r.id \
                    LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall(), len(counter)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_all_history(db: Session, page: int, limit: int, search_text=None):
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

        counter = db.execute(query).fetchall()

        if limit is not None and page is not None:
            query += f"ORDER BY h.id \
                    LIMIT {limit} OFFSET {limit * (page - 1)}"

        return db.execute(text(query)).fetchall(), len(counter)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))
