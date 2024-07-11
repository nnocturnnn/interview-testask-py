from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    age: int
    email: str

    class Config:
        orm_mode = True


class Game(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserOut(User):
    games: List[Game]


class GamesOut(Game):
    users: List[User]
