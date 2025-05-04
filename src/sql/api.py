from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.sql.queries.users import DB_Users
from src.sql.queries.characters import DB_Characters
from src.constants import Constants

engine = create_engine(Constants.DB_PATH)


class DB:
    def __init__(self):
        self.session = sessionmaker(bind=engine)()

        self.users = DB_Users(self.session)
        self.chars = DB_Characters(self.session)