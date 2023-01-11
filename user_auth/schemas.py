from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    role_id: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Joe Doe",
                "email": "joe@xyz.com",
                "password": "any",
                "role_id": "1"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "password": "any"
            }
        }
