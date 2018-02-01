"""
Token Blacklist class module.
"""

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
