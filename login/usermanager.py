from login.user import User
from login.databasemanager import DatabaseManager
from sqlalchemy import exc, orm


class UserManager:
    def __init__(self):
        dbm = DatabaseManager()
        self.session = dbm.session

    def __commit(self):
        try:
            self.session.commit()
        except exc.IntegrityError as e:
            self.session.rollback()
            print(e)

    def create_user(self, username, password):
        new_user = User(username, password)
        self.session.add(new_user)
        self.__commit()

    def delete_by_id(self, user_id):
        self.session.query(User).filter_by(id=user_id).delete()
        self.__commit()

    def delete_by_username(self, uname):
        self.session.query(User).filter_by(username=uname).delete()
        self.__commit()

    def get_by_id(self, user_id):
        return self.session.query(User).get(user_id)

    def get_by_username(self, uname):
        try:
            return self.session.query(User).filter_by(username=uname).one()
        except orm.exc.NoResultFound as e:
            print(e)

    def get_all(self):
        return self.session.query(User).all()

