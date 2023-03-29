from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from db import models
from users.currency_rate import get_currency_rate


def update_currency_rate(db: Session):
    """ get currency rate from api and update currency rate """
    currency_rate = get_currency_rate()
    print(currency_rate)
    db_currency_rate = models.CurrencyRate(
        rub_to_usd=currency_rate['RUBUSD'],
        rub_to_eur=currency_rate['RUBEUR'],
        rub_to_uzs=currency_rate['RUBUZS'],
        updated_at=currency_rate['updated_at']
    )
    db.add(db_currency_rate)
    db.commit()
    db.refresh(db_currency_rate)
    return db_currency_rate


def get_currency_last_item(db: Session):
    """ Get last currency rate if updated_at <= 24 hours, update currency rate """
    db_currency_rate = db.query(models.CurrencyRate).order_by(models.CurrencyRate.updated_at.desc()).first()
    if not db_currency_rate:
        update_currency_rate(db)
        get_currency_last_item(db)
    if db_currency_rate.updated_at <= datetime.now() - timedelta(hours=24):
        db_currency_rate = update_currency_rate(db)

    return db_currency_rate
