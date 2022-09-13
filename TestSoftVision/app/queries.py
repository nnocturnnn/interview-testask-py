from sqlalchemy.orm import Session, joinedload

from . import models, schemas

def fetch_user_from_db(db: Session):
    return db.query(models.User).order_by(models.User.id.desc()).first()
    

def fetch_user_with_games_from_db(db: Session):
    return db.query(models.User).order_by(models.User.id.desc()).options(joinedload(models.User.games)).first()


def fetch_games_from_db(db: Session):
    return db.query(models.Game).options(joinedload(models.Game.users)).all()