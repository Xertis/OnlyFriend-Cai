from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.constants import Constants
from sqlalchemy import (
    create_engine,
    Column, Integer,
    Text, ForeignKey,
    TIMESTAMP
)


engine = create_engine(Constants.DB_PATH)
Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Text)
    current_char = Column(Integer)
    last_upd = Column(TIMESTAMP)


class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Text)


class Characters(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    owner = Column(Integer, ForeignKey("users.id"))
    img_id = Column(Text)

    start_context = Column(Text)
    context = Column(Text)

    owner_rel = relationship("Users", backref="characters")


Base.metadata.create_all(engine)
