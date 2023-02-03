from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from db import models
from users.schemas import agents as schemas


class Agent:

    @staticmethod
    def get_list(page: Optional[int],
                 limit: Optional[int],
                 db: Session, ):
        if page and limit:
            query = db.query(models.Agent). \
                filter(models.Agent.block_date == None)

            if page and limit:
                return query.offset(limit * (page - 1)).limit(limit).all()
            return query.all()

    @staticmethod
    def get_by_id(db: Session, agent_id: int):
        return db.query(models.Agent).filter(
            models.Agent.id == agent_id,
            models.Agent.block_date == None).first()

    @staticmethod
    def create(db: Session, agent: schemas.AgentCreate):
        db_agent = models.Agent(**agent.dict())
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        return db_agent

    @staticmethod
    def update(db: Session, db_agent: models.Agent, agent: schemas.AgentUpdate):
        for key, value in agent.dict().items():
            if value is not None:
                setattr(db_agent, key, value)
        db.commit()
        return db_agent

    @staticmethod
    def delete(db: Session, db_agent: models.Agent):
        db_agent.block_date = datetime.now()
        db.commit()
        return db_agent

    @staticmethod
    def get_by_user_id(db: Session, user_id: int):
        return db.query(models.Agent).filter(models.Agent.user_id == user_id).first()


class AgentDebt:
    @staticmethod
    def get_list(agent_id: int,
                 page: Optional[int],
                 limit: Optional[int],
                 db: Session):
        query = db.query(models.AgentDebt).filter(models.AgentDebt.agent_id == agent_id)
        if page and limit:
            return query.offset(limit * (page - 1)).limit(limit).all()
        return query.all()