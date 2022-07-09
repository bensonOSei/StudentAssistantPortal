from sqlite_db.database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlite_db import database


def create_database():
    return database.Base.metadata.create_all(bind = engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    except:
        db.close()