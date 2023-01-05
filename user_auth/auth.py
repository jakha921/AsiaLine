import user_auth
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret_key = 'SECRET'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return user_auth.encode(payload, self.secret_key, algorithm='HS256')

    def decode_token(self, token):
        try:
            payload = user_auth.decode(token, self.secret_key)
            return payload['sub']
        except user_auth.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature expired. Please log in again.')
        except user_auth.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token. Please log in again.')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
