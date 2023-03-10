from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from pages.views import agents
from pages.views.currency import get_currency_last_item

routers = APIRouter()


# agents
@routers.get("/agents/main")
async def get_agents(db: Session = Depends(get_db),
                     searching_text: Optional[str] = None,
                     agent_id: Optional[int] = None,
                     page: Optional[int] = None,
                     limit: Optional[int] = None,
                     # jwt: dict = Depends(JWTBearer())
                     ):
    """ Get all agents and their discounts """
    # if not check_permissions('agents_main', jwt):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_agents, counter = agents.get_agents_discounts(db, agent_id, page, limit, searching_text)
        return {
            "currency": get_currency_last_item(db),
            'agents_count': counter,
            'agents': db_agents
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/agents/discounts")
async def get_discounts(db: Session = Depends(get_db),
                        searching_text: Optional[str] = None,
                        page: Optional[int] = None,
                        limit: Optional[int] = None,
                        # jwt: dict = Depends(JWTBearer())
                        ):
    """ get all discounts that can be assigned to agents """
    # if not check_permissions('agents_discounts', jwt):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        agent_discount, counter = agents.get_discounts(db, searching_text, page, limit)
        return {
            'agent_count': counter,
            'agent': agent_discount
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
