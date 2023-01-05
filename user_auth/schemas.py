from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    role: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Joe Doe",
                "email": "joe@xyz.com",
                "password": "any",
                "role": "admin"
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
