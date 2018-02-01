"""
User class module.
"""

from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
flask_bcrypt = Bcrypt(app)

class User():
    """
    User class.
    """
    def __init__(self, email, password):
        self.email = email
        self.password_hash = self.gen_hash(password)

    def gen_hash(self, string):
        """
        Generates a hash of given string and returns the hash
        """
        return flask_bcrypt.generate_password_hash(
            password=string,
            rounds=12
        ).decode('utf-8')

    def compare_candidate_with_password(self, candidate_password):
        """
        Compares candidate password with class password hash
        """
        return flask_bcrypt.check_password_hash(
            pw_hash=self.password_hash,
            password=candidate_password
        )

if __name__ == '__main__':
    username = 'username'
    password = 'password'
    user = User(username, password)
    print(user.email)
    print(user.password_hash)
    print(user.compare_candidate_with_password('password'))