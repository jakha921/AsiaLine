from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
import logging

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from pages.views import payments
from pages.views.currency import get_currency_last_item

routers = APIRouter()


# payment
@routers.get("/payments/main")
async def get_tickets(db: Session = Depends(get_db),
                      searching_text: Optional[str] = None,
                      agent_id: Optional[int] = None,
                      from_date: Optional[date] = None,
                      to_date: Optional[date] = None,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      jwt: dict = Depends(JWTBearer())
                      ):
    """ get all payments who paid amount of agents for fill the balance """
    if not check_permissions('get_refills', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_payments, counter = payments.get_refill_by_agent_id(db, from_date, to_date, agent_id, page, limit, searching_text)
        return {
            'currency': get_currency_last_item(db),
            'payments_count': counter,
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
    if not check_permissions('get_agents_balance', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db_agent_balances, counter = payments.get_agents_balance(db, agent_id, page, limit)
    return {
        'currency': get_currency_last_item(db),
        'agent_balances_count': counter,
        'agent_balances': db_agent_balances
    }
