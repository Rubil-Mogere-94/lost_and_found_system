
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///key_tracker.db', echo=False)
Session = scoped_session(sessionmaker(bind=engine))

def init_db():
    print("Initializing database...")
    from app.models import User, Item, Claim
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")