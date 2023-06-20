from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Characters(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))
    gender = Column(String(128))
    birth_year = Column(String(128))
    eye_color = Column(String(128))
    hair_color = Column(String(128))
    height = Column(Integer)
    mass = Column(Integer)
    homeworld = Column(String(128))
    films = Column(String(255))
    skin_color = Column(String(128))
    species = Column(String(255), nullable=True)
    starships = Column(String(255), nullable=True)
    vehicles = Column(String(255), nullable=True)

    @classmethod
    def get_column_names(cls) -> list:
        keys = cls.__table__.columns.keys()
        keys.remove("id")
        return keys
