from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
import logging

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from pages import sort
from pages.views import api

routers = APIRouter()


@routers.get("/users/main")
async def get_users(db: Session = Depends(get_db),
                    searching_text: Optional[str] = None,
                    page: Optional[int] = None,
                    limit: Optional[int] = None,
                    jwt: dict = Depends(JWTBearer())):
    """ get all users with then roles """
    if not check_permissions('users_main', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_users = api.get_all_users_with_role(db, page, limit, searching_text)

        return {
            'users_count': len(db_users),
            'users': db_users
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/users/roles")
async def get_roles(db: Session = Depends(get_db),
                    searching_text: Optional[str] = None,
                    page: Optional[int] = None,
                    limit: Optional[int] = None,
                    jwt: dict = Depends(JWTBearer())):
    """ get all roles that can be assigned to users """
    if not check_permissions('users_roles', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_roles = api.get_all_roles(db, page=page, limit=limit, search_text=searching_text)
        return {
            # 'count_roles': len(db_roles),
            'roles': db_roles
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# payment
@routers.get("/payments/main")
async def get_tickets(db: Session = Depends(get_db),
                      searching_text: Optional[str] = None,
                      agent_id: Optional[int] = None,
                      from_date: Optional[date] = None,
                      to_date: Optional[date] = None,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      jwt: dict = Depends(JWTBearer())):
    """ get all payments who paid amount of agents for fill the balance """
    if not check_permissions('payments_main', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_payments = api.get_refill_by_agent_id(db, from_date, to_date, agent_id, page, limit, searching_text)
        return {
            'payments_count': len(db_payments),
            'payments': db_payments
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/payments/agents/balance")
async def get_agent_balances(db: Session = Depends(get_db),
                             agent_id: Optional[int] = None,
                             page: Optional[int] = None,
                             limit: Optional[int] = None,
                             jwt: dict = Depends(JWTBearer())):
    """ Get all agent balances or by agent id """
    if not check_permissions('payments_agents_balance', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return api.get_agents_balance(db, agent_id, page, limit)


# agents
@routers.get("/agents/main")
async def get_agents(db: Session = Depends(get_db),
                     searching_text: Optional[str] = None,
                     agent_id: Optional[int] = None,
                     page: Optional[int] = None,
                     limit: Optional[int] = None,
                     jwt: dict = Depends(JWTBearer())):
    """ Get all agents and their discounts """
    if not check_permissions('agents_main', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_agents = api.get_agents_discounts(db, agent_id, page, limit, searching_text)
        return db_agents
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/agents/discounts")
async def get_discounts(db: Session = Depends(get_db),
                        searching_text: Optional[str] = None,
                        page: Optional[int] = None,
                        limit: Optional[int] = None,
                        jwt: dict = Depends(JWTBearer())):
    """ get all discounts that can be assigned to agents """
    if not check_permissions('agents_discounts', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        return api.get_discounts(db, searching_text, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# airports
@routers.get("/guide")
async def get_airports(db: Session = Depends(get_db),
                       searching_text: Optional[str] = None,
                       page: Optional[int] = None,
                       limit: Optional[int] = None):
    """ get all airports """
    try:
        db_guide = api.get_guiede(db, searching_text, page, limit)
        return {
            # 'airports_count': len(db_guide),
            'guide': db_guide
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# ticket classes
@routers.get("/guide/ticket_classes")
async def get_ticket_classes(db: Session = Depends(get_db)):
    """ get all ticket classes """
    try:
        db_classes = api.get_ticket_classes(db)
        return {
            'ticket_classes_count': len(db_classes),
            'ticket_classes': db_classes
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
