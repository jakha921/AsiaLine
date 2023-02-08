from typing import Optional

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
import logging

from db.database import get_db
from crud_models.schemas import company as schemas
from crud_models.views.company import Company
from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions, get_user_id

routers = APIRouter()


# region Company
@routers.get("/company", tags=["company"])
async def get_companies(company_id: Optional[int] = None,
                        page: Optional[int] = None,
                        limit: Optional[int] = None,
                      # jwt: dict = Depends(JWTBearer()),
                      db: Session = Depends(get_db)):
    # if not check_permissions("get_flights", jwt):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        if company_id is None:
            return Company.get_list(db, page, limit)
        else:
            db_company = Company.get_by_id(db, company_id)
            if db_company is None:
                raise ValueError("Company not found")
            return schemas.Company.from_orm(db_company)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/company", tags=["company"])
async def create_company(company: schemas.CompanyCreate,
                         # jwt: dict = Depends(JWTBearer()),
                         db: Session = Depends(get_db)):
    # if not check_permissions("create_company", jwt):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_company = Company.create(db, company)
        return schemas.Company.from_orm(db_company)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

# endregion
