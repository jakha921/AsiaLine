from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
import logging

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from pages.views.currency import get_currency_last_item
from pages.views.tickets import get_tickets_by_flight

routers = APIRouter()


@routers.get("/tickets/main")
async def get_tickets(db: Session = Depends(get_db),
                      searching_text: Optional[str] = None,
                      from_date: Optional[date] = None,
                      to_date: Optional[date] = None,
                      agent_id: Optional[int] = None,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      jwt: dict = Depends(JWTBearer())
                      ):
    """ Get tickets by flights where departure date is not past now """
    if not check_permissions('tickets_page', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_tickets, counter = get_tickets_by_flight(db, from_date=from_date, to_date=to_date,
                                                    page=page, limit=limit,
                                                    search_text=searching_text, agent_id=agent_id)
        result = {
            'currency': get_currency_last_item(db),
            'tickets_count': counter,
            'tickets': db_tickets,
        }
        return result
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
