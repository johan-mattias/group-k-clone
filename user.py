from sqlalchemy import Column, Integer, String, Sequence, Binary
from base import Base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import bcrypt


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    _password = Column(Binary(60), nullable=False)

    def __init__(self, username, plaintext_password):
        self.username = username
        self.password = plaintext_password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.hashpw(plaintext_password.encode('utf8'), bcrypt.gensalt(15))

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.checkpw(plaintext_password, self.password)