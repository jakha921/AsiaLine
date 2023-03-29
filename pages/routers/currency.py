import logging

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from pages.views.currency import get_currency_last_item

routers = APIRouter()


def sort_currency_rate(currency_rate):
    dict_currency_rate = {
        "RUBUSD": currency_rate.rub_to_usd,
        "RUBEUR": currency_rate.rub_to_eur,
        "RUBUZS": currency_rate.rub_to_uzs,
        "updated_at": currency_rate.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    }

    return dict_currency_rate


@routers.get("/currency_rate", tags=["pages"])
async def get_currency_rate(db: Session = Depends(get_db)):
    """ Get currency rate from api and update currency rate """
    try:
        return get_currency_last_item(db)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
