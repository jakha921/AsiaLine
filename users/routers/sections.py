from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from db.database import get_db
from users.schemas import sections as schemas
from users.views.sections import Section

routers = APIRouter()


@routers.get("/sections", response_model=list[schemas.Section], tags=["sections"])
async def get_sections_list(
        page: Optional[int] = None,
        limit: Optional[int] = None,
        db: Session = Depends(get_db)):
    try:
        return Section.get_list(page, limit, db)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/section/{section_id}", tags=["sections"])
async def get_section(section_id: int,
                      db: Session = Depends(get_db)):
    try:
        db_section = Section.get_by_id(db, section_id)
        if db_section is None:
            raise ValueError("Section not found")
        return schemas.Section.from_orm(db_section)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/section", tags=["sections"])
async def create_section(section: schemas.SectionCreate,
                         db: Session = Depends(get_db)):
    try:
        return schemas.Section.from_orm(Section.create(db, section))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/section/{section_id}", tags=["sections"])
async def update_section(section_id: int,
                         section: schemas.SectionUpdate,
                         db: Session = Depends(get_db)):
    try:
        db_section = Section.get_by_id(db, section_id)
        if db_section is None:
            raise ValueError("Section not found")
        return schemas.Section.from_orm(Section.update(db, db_section, section))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/section/{section_id}", tags=["sections"])
async def delete_section(section_id: int,
                         db: Session = Depends(get_db)):
    try:
        db_section = Section.get_by_id(db, section_id)
        if db_section is None:
            raise ValueError("Section not found")
        return Section.delete(db, section_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
