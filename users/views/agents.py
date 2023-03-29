from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from auth.hashing import decode_password, encode_password
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
                         models.Agent.address, models.Agent.phone, models.Agent.is_on_credit,
                         models.Agent.discount_id, models.Agent.registered_date, models.Agent.block_date,
                         models.Agent.user_id, models.User.email, models.User.password). \
            filter(models.Agent.block_date == None). \
            join(models.User, models.Agent.user_id == models.User.id)
        if page and limit:
            return query.offset(limit * (page - 1)).limit(limit).all()
        return query.all()

    @staticmethod
    def get_by_id(db: Session, agent_id: int):
        query = db.query(models.Agent.id, models.Agent.company_name, models.Agent.balance,
                         models.Agent.address, models.Agent.phone, models.Agent.is_on_credit,
                         models.Agent.discount_id, models.Agent.registered_date, models.Agent.block_date,
                         models.Agent.user_id, models.User.email, models.User.password). \
            filter(models.Agent.block_date == None,
                   models.Agent.id == agent_id). \
            join(models.User, models.Agent.user_id == models.User.id).first()
        return query

    @staticmethod
    def get_by_id_without_join(db: Session, agent_id: int):
        agent = db.query(models.Agent).filter(models.Agent.block_date == None, models.Agent.id == agent_id).first()
        user = User.get_by_id(db, agent.user_id)
        return agent, user

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
        old_agent, old_user = db_agent
        query = {}

        if agent.email and old_user.email != agent.email:
            query['email'] = agent.email if agent.email else old_user.email

        if agent.password and old_user.password != encode_password(agent.password):
            query['password'] = agent.password if agent.password else old_user.password

        if agent.company_name and old_agent.company_name != agent.company_name:
            query['username'] = agent.company_name if agent.company_name else old_agent.company_name

        query['role_id'] = 3

        if query:
            fields = ['email', 'password', 'username', 'role_id']
            user_update = UserUpdate(
                **{key: query[key] for key in query if key in fields}
            )
            User.update(db, old_agent.user_id, user_update)

        for key, value in agent.dict().items():
            if value is not None:
                setattr(old_agent, key, value)
        db.commit()
        db.refresh(old_agent)
        return old_agent

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
                         models.AgentDebt.created_at). \
            join(models.Ticket, models.AgentDebt.ticket_id == models.Ticket.id). \
            join(models.Flight, models.Ticket.flight_id == models.Flight.id). \
            join(models.FlightGuide, models.Flight.flight_guide_id == models.FlightGuide.id). \
            filter(models.AgentDebt.agent_id == agent_id)
        if page and limit:
            return query.offset(limit * (page - 1)).limit(limit).all()
        return query.all()
