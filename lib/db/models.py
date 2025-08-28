from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from lib.db.setup import Base


trip_tag = Table(
    "trip_tag",
    Base.metadata,
    Column("trip_id", Integer, ForeignKey("trips.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    notes = Column(String)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="trips")

    tags = relationship("Tag", secondary=trip_tag, back_populates="trips")
    destinations = relationship("Destination", back_populates="trip", cascade="all, delete-orphan")

    @classmethod
    def create(cls, session, name, start=None, end=None, notes=None, category=None, tags=None):
        trip = cls(name=name, start_date=start, end_date=end, notes=notes, category=category)
        if tags:
            trip.tags.extend(tags)
        session.add(trip)
        session.commit()
        return trip

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    

    @classmethod
    def find_by_id(cls, session, trip_id):
        return session.query(cls).get(trip_id)

    def delete(self, session):
        session.delete(self)
        session.commit()


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String)
    arrival_date = Column(Date)
    departure_date = Column(Date)

    trip_id = Column(Integer, ForeignKey("trips.id"))
    trip = relationship("Trip", back_populates="destinations")
    activities = relationship("Activity", back_populates="destination", cascade="all, delete-orphan")

    @classmethod
    def create(cls, session, name, country, trip, arrival=None, departure=None):
        dest = cls(name=name, country=country, trip=trip, arrival_date=arrival, departure_date=departure)
        session.add(dest)
        session.commit()
        return dest

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, dest_id):
        return session.query(cls).get(dest_id)

    def delete(self, session):
        session.delete(self)
        session.commit()


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    activity_date = Column(Date)
    cost = Column(Float, default=0.0)



    destination_id = Column(Integer, ForeignKey("destinations.id"))
    destination = relationship("Destination", back_populates="activities")

    @classmethod
    def create(cls, session, name, destination, description=None, date=None, cost=0.0):
        act = cls(name=name, description=description, activity_date=date, cost=cost, destination=destination)
        session.add(act)
        session.commit()
        return act

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, activity_id):
        return session.query(cls).get(activity_id)

    def delete(self, session):
        session.delete(self)
        session.commit()


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


    trips = relationship("Trip", back_populates="category")

    @classmethod
    def get_or_create(cls, session, name):
        cat = session.query(cls).filter_by(name=name).first()
        if not cat:
            cat = cls(name=name)
            session.add(cat)
            session.commit()
        return cat


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    trips = relationship("Trip", secondary=trip_tag, back_populates="tags")

    @classmethod
    def get_or_create(cls, session, name):
        tag = session.query(cls).filter_by(name=name).first()
        if not tag:
            tag = cls(name=name)
            session.add(tag)
            session.commit()
        return tag

