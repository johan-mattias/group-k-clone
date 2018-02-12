"""
LoginManager class module.
"""

import datetime
import jwt
from login.token_blacklist import TokenBlacklistManager

SECRET_KEY = 'SECRET_KEY'

class LoginManager():
    """
    LoginManager class.
    """
    def __init__(self):
        self.tbm = TokenBlacklistManager()

    def encode_auth_token(self, user_id, days=7, minutes=0, seconds=0):
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

            token = jwt.encode(
                payload=payload,
                key=SECRET_KEY,
                algorithm='HS256'
            )

            return token
        except Exception as e:
            return e

    def decode_auth_token(self, token):
        try:
            payload = jwt.decode(jwt=token, key=SECRET_KEY)
            if self.tbm.check_blacklist(token):
                return 'Token blacklisted. Please log in again.'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

if __name__ == '__main__':
    login = LoginManager()
    user_id = 999
    token = login.encode_auth_token(user_id)
    print('token', token)
    payload_sub = login.decode_auth_token(auth_token=token)
    print('payload_sub', payload_sub)