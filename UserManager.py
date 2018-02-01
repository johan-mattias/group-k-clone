from user import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class UserManager:
    def __init__(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_user(self, username, password):
        new_user = User(username, password)
        self.session.add(new_user)
        self.session.commit()

    def delete_user_by_id(self, user_id):
        self.session.query(User).filter_by(id=user_id).delete()
        self.session.commit()

    def delete_user_by_username(self, uname):
        self.session.query(User).filter_by(username=uname).delete()
        self.session.commit()

    def get_user_by_id(self, user_id):
        return self.session.query(User).get(user_id)

    def get_user_by_username(self, uname):
        return self.session.query(User).filter_by(username=uname).one()
