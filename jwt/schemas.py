from pydantic import BaseModel


class AuthToken(BaseModel):
    username: str
    password: str
