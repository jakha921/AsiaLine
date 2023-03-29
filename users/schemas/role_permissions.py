from pydantic import BaseModel, validator


class RolePermissionCreate(BaseModel):
    role_id: int
    permission_id: int

    @validator('role_id')
    def role_id_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('role_id must be positive')
        return v

    @validator('permission_id')
    def permission_id_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('permission_id must be positive')
        return v

    class Config:
        schema_extra = {
            "example": {
                "role_id": 1,
                "permission_id": 1,
            }
        }


class RolePermissionUpdate(RolePermissionCreate):
    pass


class RolePermission(RolePermissionCreate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **RolePermissionCreate.Config.schema_extra.get("example"),
            }
        }
