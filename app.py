from user import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)


def main():
    Session = sessionmaker(bind=engine)
    session = Session()
    user1 = User(username="Anton", plaintext_password="asdf")
    session.add(user1)
    session.commit()
    user1get = session.query(User).get(1)
    print(user1get.id, user1get.username, user1get.password)


if __name__ == "__main__":
    main()