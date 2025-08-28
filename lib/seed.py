from models import Trip, Destination, Activity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///travel_journal.db")
Session = sessionmaker(bind=engine)
session = Session()

trip1 = Trip(name="Europe Summer 2025")

dest1 = Destination(city="Paris", country="France", trip=trip1)
dest2 = Destination(city="Rome", country="Italy", trip=trip1)

act1 = Activity(name="Visited the Louvre", destination=dest1)
act2 = Activity(name="Climbed the Eiffel Tower", destination=dest1)
act3 = Activity(name="Colosseum Tour", destination=dest2)

session.add_all([trip1, dest1, dest2, act1, act2, act3])

session.commit()

print("✅ Seeding complete!")
