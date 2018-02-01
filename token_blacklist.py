"""
Token Blacklist class module.
"""

import datetime
import jwt

SECRET_KEY = 'SECRET_KEY'

class TokenBlacklist():
    """
    Token Blacklist class.
    """
    def __init__(self):
        pass

    @staticmethod
    def check_blacklist(auth_token):
        """
        Check whether token is blacklisted
        """
        # TODO: sql query in blacklist table to find token
        res = False
        if res:
            return True
        else:
            return False

if __name__ == '__main__':
    login = Login()
    user_id = 1
    token = login.encode_auth_token(user_id)
    print('token', token)
    payload_sub = login.decode_auth_token(token)
    print('payload_sub', payload_sub)