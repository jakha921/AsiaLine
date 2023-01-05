import logging
import traceback

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from users import crud, schemas
from db.database import get_db

routers = APIRouter()


# region Roles
@routers.get("/roles", response_model=list[schemas.Role])
async def get_all_roles(min: Optional[int] = 0, max: Optional[int] = 10, db: Session = Depends(get_db)):
    """ Get list of roles """
    return crud.Role.get_list(db, min, max)


@routers.get("/role/{role_id}", response_model=schemas.Role)
async def get_role(role_id: int, db: Session = Depends(get_db)):
    """ get role by given id """
    db_role = crud.Role.get_by_id(db, role_id)
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return db_role


@routers.post("/role", response_model=schemas.Role)
async def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return crud.Role.create(db, role)


@routers.patch("/role/{role_id}", response_model=schemas.Role)
async def update_role(role_id: int, role: schemas.RoleUpdate, db: Session = Depends(get_db)):
    db_role = crud.Role.get_by_id(db, role_id)
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return crud.Role.update(db, role_id, role)


@routers.delete("/role/{role_id}", response_model=schemas.Role)
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = crud.Role.get_by_id(db, role_id)
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return crud.Role.delete(db, role_id)


# endregion Roles


# region User
@routers.get("/users", response_model=list[schemas.User])
async def get_users_list(min: Optional[int] = 0, max: Optional[int] = 10, db: Session = Depends(get_db)):
    return crud.User.get_list(db, min, max)


@routers.get("/user/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = crud.User.get_by_id(db, user_id)
        return db_user
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/user", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.User.get_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        return crud.User.create(db, user)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/user/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    try:
        db_user = crud.User.get_by_id(db, user_id)

        # Check if user exists in db by email
        if user.email:
            db_user_by_email = crud.User.get_by_email(db, user.email)
            if db_user_by_email and db_user_by_email.id != user_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return crud.User.update(db, user_id, user)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = crud.User.get_by_id(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return crud.User.delete(db, user_id)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion User


# region Section
@routers.get("/sections", response_model=list[schemas.Section])
async def get_sections_list(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.Section.get_list(db, min, max)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/section/{section_id}", response_model=schemas.Section)
async def get_section(section_id: int, db: Session = Depends(get_db)):
    try:
        db_section = crud.Section.get_by_id(db, section_id)
        if db_section is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
        return db_section
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/section", response_model=schemas.Section)
async def create_section(section: schemas.SectionCreate, db: Session = Depends(get_db)):
    try:
        return crud.Section.create(db, section)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/section/{section_id}", response_model=schemas.Section)
async def update_section(section_id: int, section: schemas.SectionUpdate, db: Session = Depends(get_db)):
    try:
        db_section = crud.Section.get_by_id(db, section_id)
        if db_section is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
        return crud.Section.update(db, section_id, section)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/section/{section_id}")
async def delete_section(section_id: int, db: Session = Depends(get_db)):
    try:
        db_section = crud.Section.get_by_id(db, section_id)
        if db_section is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
        return crud.Section.delete(db, section_id)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion Section


# region Permission
@routers.get("/permissions")
async def get_permissions_list(min: Optional[int] = 0, max: Optional[int] = 10, db: Session = Depends(get_db)):
    return crud.Permission.get_list(db, min, max)


@routers.get("/permission/{permission_id}")
async def get_permission(permission_id: int, db: Session = Depends(get_db)):
    try:
        db_permission = crud.Permission.get_by_id(db, permission_id)
        if db_permission is None:
            return {"detail": "Permission not found"}
        return db_permission
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/permission", response_model=schemas.Permission)
async def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(get_db)):
    return crud.Permission.create(db, permission)


@routers.patch("/permission/{permission_id}", response_model=schemas.Permission)
async def update_permission(permission_id: int, permission: schemas.PermissionUpdate, db: Session = Depends(get_db)):
    try:
        db_permission = crud.Permission.get_by_id(db, permission_id)
        if db_permission is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        return crud.Permission.update(db, permission_id, permission)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/permission/{permission_id}", response_model=schemas.Permission)
async def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    try:
        db_permission = crud.Permission.get_by_id(db, permission_id)
        if db_permission is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        return crud.Permission.delete(db, permission_id)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion Permission


# region Role Permission
@routers.get("/role_permissions", response_model=list[schemas.RolePermission])
async def get_role_permissions_list(min: Optional[int] = 0, max: Optional[int] = 10, db: Session = Depends(get_db)):
    try:
        return crud.RolePermission.get_list(db, min, max)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/role_permission/{role_permission_id}")
async def get_role_permission(role_permission_id: int, db: Session = Depends(get_db)):
    try:
        db_role_permission = crud.RolePermission.get_by_id(db, role_permission_id)
        if db_role_permission is None:
            return {"detail": "Group permission not found"}
        return db_role_permission
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/role_permission", response_model=schemas.RolePermission)
async def create_role_permission(role_permission: schemas.RolePermissionCreate, db: Session = Depends(get_db)):
    try:
        return crud.RolePermission.create(db, role_permission)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/role_permission/{role_permission_id}", response_model=schemas.RolePermission)
async def update_role_permission(role_permission_id: int, role_permission: schemas.RolePermissionUpdate,
                                 db: Session = Depends(get_db)):
    try:
        db_role_permission = crud.RolePermission.get_by_id(db, role_permission_id)
        if db_role_permission is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group permission not found")
        return crud.RolePermission.update(db, role_permission_id, role_permission)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/role_permission/{role_permission_id}")
async def delete_role_permission(role_permission_id: int, db: Session = Depends(get_db)):
    try:
        db_role_permission = crud.RolePermission.get_by_id(db, role_permission_id)
        if db_role_permission is None:
            return {"detail": "Group permission not found"}
        return crud.RolePermission.delete(db, role_permission_id)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion Group Permission


# region Agent
@routers.get("/agents", response_model=list[schemas.Agent])
async def get_agents_list(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.Agent.get_list(db, min, max)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/agent/{agent_id}", response_model=schemas.Agent)
async def get_agent(agent_id: int, db: Session = Depends(get_db)):
    try:
        db_agent = crud.Agent.get_by_id(db, agent_id)
        if db_agent is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
        return db_agent
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/agent", response_model=schemas.Agent)
async def create_agent(agent: schemas.AgentCreate, db: Session = Depends(get_db)):
    try:
        return crud.Agent.create(db, agent)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/agent/{agent_id}", response_model=schemas.Agent)
async def update_agent(agent_id: int, agent: schemas.AgentUpdate, db: Session = Depends(get_db)):
    try:
        db_agent = crud.Agent.get_by_id(db, agent_id)
        if db_agent is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
        return crud.Agent.update(db, agent_id, agent)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/agent/{agent_id}")
async def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    try:
        db_agent = crud.Agent.get_by_id(db, agent_id)
        if db_agent is None:
            return {"detail": "Agent not found"}
        return crud.Agent.delete(db, agent_id)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion Agent


# region Discount
@routers.get("/discounts", response_model=list[schemas.Discount])
async def get_discounts_list(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.Discount.get_list(db, min, max)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/discount/{discount_id}", response_model=schemas.Discount)
async def get_discount(discount_id: int, db: Session = Depends(get_db)):
    try:
        db_discount = crud.Discount.get_by_id(db, discount_id)
        if db_discount is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")
        return db_discount
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/discount", response_model=schemas.Discount)
async def create_discount(discount: schemas.DiscountCreate, db: Session = Depends(get_db)):
    try:
        return crud.Discount.create(db, discount)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/discount/{discount_id}", response_model=schemas.Discount)
async def update_discount(discount_id: int, discount: schemas.DiscountUpdate, db: Session = Depends(get_db)):
    try:
        db_discount = crud.Discount.get_by_id(db, discount_id)
        if db_discount is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")
        return crud.Discount.update(db, discount_id, discount)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/discount/{discount_id}")
async def delete_discount(discount_id: int, db: Session = Depends(get_db)):
    try:
        db_discount = crud.Discount.get_by_id(db, discount_id)
        if db_discount is None:
            return {"detail": "Discount not found"}
        return crud.Discount.delete(db, discount_id)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# endregion Discount
