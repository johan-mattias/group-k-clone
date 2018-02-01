from sqlalchemy import create_engine, orm
from base import Base

PATH_TO_DATABASE = "test.db"


class DatabaseManager:
    def __init__(self):
        engine = create_engine('sqlite:///' + PATH_TO_DATABASE)
        Base.metadata.create_all(engine)
        Session = orm.sessionmaker(bind=engine)

        self.session = Session()