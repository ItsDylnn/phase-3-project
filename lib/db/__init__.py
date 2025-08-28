from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base 

def init_db():
    engine = create_engine("sqlite:///travel_journal.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
