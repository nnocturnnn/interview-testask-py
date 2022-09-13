from fastapi import Depends, FastAPI, status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from faker import Faker
import random

from .database import SessionLocal, engine

from . import models, schemas, queries

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

fake = Faker()


def load_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/" ,status_code=status.HTTP_200_OK)
def index():
    return ""


@app.get("/get_games", response_model=schemas.GamesOut)
def featch_games():
    games = queries.fetch_games_from_db(db)
    return games

@app.get("/get_me", response_model=schemas.User)
def featch_user(db: Session = Depends(load_db)):
    user = queries.fetch_user_with_games_from_db(db)
    back_schemas = schemas.UserOut.from_orm(user)
    return back_schemas
    

@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(db: Session = Depends(load_db)):
    db_user = models.User(name=fake.name(), age=random.randint(1, 100), email=fake.email())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/create_game", status_code=status.HTTP_201_CREATED)
def create_game(db: Session = Depends(load_db)):
    db_game = models.Game(name=fake.company())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@app.post("/connect_to_game",  response_model=schemas.Game ,status_code=status.HTTP_201_CREATED)
def create_connect(game: schemas.Game, db: Session = Depends(load_db)):
    user = queries.fetch_user_from_db(db)
    game = models.Game(**game.dict())
    user.games.append(game)
    return game


if __name__ == "__main__":
    from fastapi.testclient import TestClient

    client = TestClient(api)
    data  = """{"name" : "Diablo 3"}"""
    response = client.post("/create_user")
    response = client.post("/connect_to_game")
    response = client.get("/get_games")
    print(response)

    
    
    
