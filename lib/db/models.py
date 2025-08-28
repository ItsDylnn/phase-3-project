from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Table

Base = declarative_base()

trip_tags = Table(
    "trip_tags",
    Base.metadata,
    Column("trip_id", Integer, ForeignKey("trips.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    notes = Column(String, nullable=True)

    destinations = relationship("Destination", back_populates="trip", cascade="all, delete-orphan")
    activities = relationship("Activity", secondary="destinations", viewonly=True)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="trips")

    tags = relationship("Tag", secondary=trip_tags, back_populates="trips")

    @staticmethod
    def create(session, name, start=None, end=None, notes=None, category=None, tags=None):
        trip = Trip(name=name, start_date=start, end_date=end, notes=notes, category=category)
        if tags:
            trip.tags = tags
        session.add(trip)
        session.commit()
        return trip

    @staticmethod
    def get_all(session):
        return session.query(Trip).all()

    @staticmethod
    def find_by_id(session, trip_id):
        return session.query(Trip).get(trip_id)

    def delete(self, session):
        session.delete(self)
        session.commit()

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    arrival_date = Column(Date, nullable=True)
    departure_date = Column(Date, nullable=True)

    trip_id = Column(Integer, ForeignKey("trips.id"))
    trip = relationship("Trip", back_populates="destinations")
    activities = relationship("Activity", back_populates="destination", cascade="all, delete-orphan")

    @staticmethod
    def create(session, name, country, trip, arrival=None, departure=None):
        dest = Destination(name=name, country=country, trip=trip, arrival_date=arrival, departure_date=departure)
        session.add(dest)
        session.commit()
        return dest

    @staticmethod
    def get_all(session):
        return session.query(Destination).all()

    @staticmethod
    def find_by_id(session, dest_id):
        return session.query(Destination).get(dest_id)

    def delete(self, session):
        session.delete(self)
        session.commit()

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    activity_date = Column(Date, nullable=True)
    cost = Column(Float, default=0.0)

    destination_id = Column(Integer, ForeignKey("destinations.id"))
    destination = relationship("Destination", back_populates="activities")

    @staticmethod
    def create(session, name, destination, description=None, date=None, cost=0.0):
        act = Activity(name=name, destination=destination, description=description, activity_date=date, cost=cost)
        session.add(act)
        session.commit()
        return act

    @staticmethod
    def get_all(session):
        return session.query(Activity).all()

    @staticmethod
    def find_by_id(session, act_id):
        return session.query(Activity).get(act_id)

    def delete(self, session):
        session.delete(self)
        session.commit()

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    trips = relationship("Trip", back_populates="category")

    @staticmethod
    def get_or_create(session, name):
        category = session.query(Category).filter_by(name=name).first()
        if not category:
            category = Category(name=name)
            session.add(category)
            session.commit()
        return category

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    trips = relationship("Trip", secondary=trip_tags, back_populates="tags")

    @staticmethod
    def get_or_create(session, name):
        tag = session.query(Tag).filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name)
            session.add(tag)
            session.commit()
        return tag
