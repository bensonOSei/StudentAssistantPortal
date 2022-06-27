from database import SessionLocal, engine
import database
import db_models
from sqlalchemy.orm import Session


def create_database():
    return database.Base.metadata.create_all(bind = engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    except:
        db.close()