from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from users.schemas import agents as schemas
from users.views.agents import Agent, AgentDebt

routers = APIRouter()


@routers.get("/agents", tags=["agents"])
async def get_agents_list(page: Optional[int] = None,
                          limit: Optional[int] = None,
                          db: Session = Depends(get_db)):
    try:
        return Agent.get_list(page, limit, db)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/agent/{agent_id}", tags=["agents"])
async def get_agent(agent_id: int,
                    db: Session = Depends(get_db)):
    try:
        db_agent = Agent.get_by_id(db, agent_id)
        if db_agent is None:
            raise ValueError("Agent not found")
        return db_agent
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/agent", tags=["agents"])
async def create_agent(agent: schemas.AgentCreate,
                       jwt: dict = Depends(JWTBearer()),
                       db: Session = Depends(get_db)):
    if not check_permissions('create_agent', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        if Agent.get_by_email(db, agent.email):
            raise ValueError("This user is already an agent")
        return schemas.Agent.from_orm(Agent.create(db, agent))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/agent/{agent_id}", tags=["agents"])
async def update_agent(agent_id: int,
                       agent: schemas.AgentUpdate,
                       jwt: dict = Depends(JWTBearer()),
                       db: Session = Depends(get_db)):
    if not check_permissions('update_agent', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        db_agent = Agent.get_by_id_without_join(db, agent_id)
        old_agent, old_user = db_agent
        if old_agent is None:
            raise ValueError("Agent not found")
        if old_user.email != agent.email and Agent.get_by_email(db, agent.email):
            raise ValueError("This user is already an agent")
        return Agent.update(db, db_agent, agent)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/agent/{agent_id}", tags=["agents"])
async def delete_agent(agent_id: int,
                       jwt: dict = Depends(JWTBearer()),
                       db: Session = Depends(get_db)):
    if not check_permissions('delete_agent', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        db_agent = Agent.get_by_id_without_join(db, agent_id)
        if db_agent[0] is None:
            raise ValueError("Agent not found")
        return Agent.delete(db, db_agent[0])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# Agent Debt
@routers.get("/agent_debts/{agent_id}", tags=['agents'])
async def get_agent_debts(agent_id: int,
                          page: Optional[int] = None,
                          limit: Optional[int] = None,
                          db: Session = Depends(get_db)):
    try:
        return AgentDebt.get_list(agent_id, page, limit, db)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
