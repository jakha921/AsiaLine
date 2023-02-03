from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from db.database import get_db
from crud_models.schemas import scraped_price as schemas
from crud_models.views.scraped_price import ScrapedPrice

routers = APIRouter()


@routers.get("/scraped_prices", response_model=list[schemas.ScrapedPrice], tags=["scraped_prices"])
async def get_scraped_prices(page: Optional[int] = None,
                             limit: Optional[int] = None,
                             db: Session = Depends(get_db)):
    """ Get scraped prices list """
    try:
        return ScrapedPrice.get_list(db, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Internal server error get scraped prices")


@routers.get("/scraped_price/{scraped_price_id}", tags=["scraped_prices"])
async def get_scraped_price(scraped_price_id: int,
                            db: Session = Depends(get_db)):
    """ Get scraped price by id """
    try:
        db_scraped_price = ScrapedPrice.get_by_id(db, scraped_price_id)
        if db_scraped_price is None:
            raise ValueError("Scraped price not found")
        return schemas.ScrapedPrice.from_orm(db_scraped_price)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bad request")


@routers.post("/scraped_price", tags=["scraped_prices"])
async def create_scraped_price(scraped_price: schemas.ScrapedPriceCreate,
                               db: Session = Depends(get_db)):
    """ Create scraped price """
    try:
        return ScrapedPrice.create(db, scraped_price)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/scraped_price/{scraped_price_id}", tags=["scraped_prices"])
async def update_scraped_price(scraped_price_id: int,
                               scraped_price: schemas.ScrapedPriceUpdate,
                               db: Session = Depends(get_db)):
    try:
        db_scraped_price = ScrapedPrice.get_by_id(db, scraped_price_id)
        if db_scraped_price is None:
            raise ValueError("Scraped price not found")
        return ScrapedPrice.update(db, db_scraped_price, scraped_price)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/scraped_price/{scraped_price_id}", tags=["scraped_prices"])
async def delete_scraped_price(scraped_price_id: int, db: Session = Depends(get_db)):
    try:
        db_scraped_price = ScrapedPrice.get_by_id(db, scraped_price_id)
        if db_scraped_price is None:
            raise ValueError("Scraped price not found")
        return ScrapedPrice.delete(db, db_scraped_price)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
