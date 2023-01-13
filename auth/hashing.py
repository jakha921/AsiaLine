# encode and decode password
import base64


def encode_password(password):
    return base64.b64encode(password.encode()).decode()


def decode_password(encoded_password):
    return base64.b64decode(encoded_password.encode()).decode()
