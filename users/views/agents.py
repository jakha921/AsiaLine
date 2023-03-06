from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from auth.hashing import decode_password
from db import models
from users.schemas import agents as schemas
from users.views.users import User
from users.schemas.users import UserCreate, UserUpdate


class Agent:

    @staticmethod
    def get_list(page: Optional[int],
                 limit: Optional[int],
                 db: Session, ):
        query = db.query(models.Agent.id, models.Agent.company_name, models.Agent.balance,
                         models.Agent.address, models.Agent.phone, models.Agent.registered_date,
                         models.Agent.is_on_credit, models.Agent.discount_id, models.Agent.block_date,
                         models.User.email,
                         models.User.password). \
            filter(models.Agent.block_date == None). \
            join(models.User, models.Agent.user_id == models.User.id)
        if page and limit:
            return query.offset(limit * (page - 1)).limit(limit).all()
        return query.all()

    @staticmethod
    def get_by_id(db: Session, agent_id: int):
        query = db.query(models.Agent.id, models.Agent.company_name, models.Agent.balance,
                         models.Agent.address, models.Agent.phone, models.Agent.registered_date,
                         models.Agent.is_on_credit, models.Agent.discount_id, models.Agent.block_date,
                         models.User.email,
                         models.User.password). \
            filter(models.Agent.block_date == None,
                   models.Agent.id == agent_id). \
            join(models.User, models.Agent.user_id == models.User.id).first()

        # if query:
        #     # decode user password
        #     query.password = decode_password(query.password)

        return query

    @staticmethod
    def create(db: Session, agent: schemas.AgentCreate):
        user = User.create(db, UserCreate(
            email=agent.email,
            password=agent.password,
            username=agent.company_name,
            role_id=3,
        ))

        agent = agent.dict()
        agent.pop('email')
        agent.pop('password')
        agent['user_id'] = user.id

        db_agent = models.Agent(**agent)
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        return db_agent

    @staticmethod
    def update(db: Session, db_agent: models.Agent, agent: schemas.AgentUpdate):
        if db_agent.user.email != agent.email or db_agent.user.password != agent.password:
            User.update(db, db_agent.user_id, UserUpdate(
                email=agent.email if agent.email else db_agent.user.email,
                password=agent.password if agent.password else db_agent.user.password,
                username=agent.company_name if agent.company_name else db_agent.user.username,
                role_id=3,
            ))

        agent = agent.dict()
        agent.pop('email')
        agent.pop('password')
        print(agent)
        for key, value in agent.items():
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
    def get_by_email(db: Session, email: str):
        """ get user by email and check is this user is agent or not """
        return db.query(
            models.Agent
        ).filter(
            models.User.email == email,
            models.Agent.user_id == models.User.id,
        ).first()


class AgentDebt:
    @staticmethod
    def get_list(agent_id: int,
                 page: Optional[int],
                 limit: Optional[int],
                 db: Session):
        query = db.query(models.Ticket.ticket_number, models.FlightGuide.flight_number,
                         models.AgentDebt.type, models.AgentDebt.amount, models.AgentDebt.comment,
                         models.AgentDebt.created_at).\
            join(models.Ticket, models.AgentDebt.ticket_id == models.Ticket.id).\
            join(models.Flight, models.Ticket.flight_id == models.Flight.id).\
            join(models.FlightGuide, models.Flight.flight_guide_id == models.FlightGuide.id).\
            filter(models.AgentDebt.agent_id == agent_id)
        if page and limit:
            return query.offset(limit * (page - 1)).limit(limit).all()
        return query.all()
