from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import exc, orm
from base import Base
import datetime
from databasemanager import DatabaseManager

class _TokenBlacklist(Base):
    __tablename__ = 'blacklist_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(5000), unique=True, nullable=False)
    blacklisted_on = Column(DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

class TokenBlacklistManager():
    def __init__(self):
        dbm = DatabaseManager()
        self.session = dbm.session

    def __commit(self):
        try:
            self.session.commit()
        except exc.IntegrityError as e:
            self.session.rollback()
            print(e)

    def blacklist_token(self, token):
        new_token = _TokenBlacklist(token)
        self.session.add(new_token)
        self.__commit()

    def check_blacklist(self, token):
        try:
            return self.session.query(_TokenBlacklist).filter_by(token=token.encode('utf-8')).one().token
        except orm.exc.NoResultFound:
            return False

if __name__ == '__main__':
    tknm = TokenBlacklistManager()
    tknm.blacklist_token('123')
    print(tknm.check_blacklist('123'))