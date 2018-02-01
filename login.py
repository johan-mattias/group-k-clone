"""
Login class module.
"""

import datetime
import jwt

SECRET_KEY = 'SECRET_KEY'

class Login():
    """
    Login class.
    """
    def __init__(self):
        pass

    def encode_auth_token(self, user_id, days=0, minutes=0, seconds=0):
        """
        Generates auth token
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() +
                    datetime.timedelta(days=days, minutes=minutes, seconds=seconds),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            print('payload', payload)
            return jwt.encode(
                payload=payload,
                key=SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates auth token
        """
        try:
            payload = jwt.decode(jwt=auth_token, key=SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

if __name__ == '__main__':
    login = Login()
    user_id = 1
    token = login.encode_auth_token(user_id)
    print('token', token)
    payload_sub = login.decode_auth_token(token)
    print('payload_sub', payload_sub)