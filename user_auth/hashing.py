# password encode and decode
import base64

encoded = 'MTIzNDU2Nzg='
decoded = '12345678'


def encode_password(password):
    return base64.b64encode(password.encode()).decode()


def decode_password(encoded_password):
    return base64.b64decode(encoded_password.encode()).decode()


def verify_password(password, encoded_password):
    return password == decode_password(encoded_password)


if __name__ == '__main__':
    print('encode', encode_password(decoded), decoded)
    print('decode', decode_password(encoded), encoded)
    print('verify', verify_password(decoded, encoded))
