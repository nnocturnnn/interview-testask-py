from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


association_table = Table(
    "association",
    Base.metadata,
    Column("users_id", ForeignKey("users.id"), primary_key=True),
    Column("games_id", ForeignKey("games.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True)
    email = Column(String, unique=True, index=True)

    game = relationship("Game", secondary=association_table, back_populates="users")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    user = relationship("User", secondary=association_table, back_populates="games")