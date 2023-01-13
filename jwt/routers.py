from fastapi import FastAPI, Depends, HTTPException, APIRouter
from jwt.auth import AuthHandler
from jwt.schemas import AuthToken

router = APIRouter()

auth_handler = AuthHandler()
user = []


@router.post("/register", status_code=201)
def register(auth: AuthToken):
    if any(x['username'] == auth.username for x in user):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth.password)
    user.append({'username': auth.username, 'password': hashed_password})
    return {'message': 'User created successfully'}

@router.post("/login")
def login(auth: AuthToken):
    user_ = [x for x in user if x['username'] == auth.username]
    if not user_:
        raise HTTPException(status_code=404, detail='User not found')
    if not auth_handler.verify_password(auth.password, user_[0]['password']):
        raise HTTPException(status_code=400, detail='Incorrect password')
    return {'access_token': auth_handler.encode_token(auth.username)}

@router.get("/unprotected")
def unprotected():
    return {"message": "unprotected endpoint"}

@router.get("/protected")
def protected(username: str = Depends(auth_handler.auth_wrapper)):
    return {"message": "protected endpoint"}