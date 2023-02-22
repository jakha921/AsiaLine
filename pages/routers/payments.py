from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
import logging

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from pages.views import payments

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
                      # jwt: dict = Depends(JWTBearer())
                      ):
    """ get all payments who paid amount of agents for fill the balance """
    # if not check_permissions('payments_main', jwt):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_payments = payments.get_refill_by_agent_id(db, from_date, to_date, agent_id, page, limit, searching_text)
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
                             # jwt: dict = Depends(JWTBearer())
                             ):
    """ Get all agent balances or by agent id """
    # if not check_permissions('payments_agents_balance', jwt):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return payments.get_agents_balance(db, agent_id, page, limit)