from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float,Table, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship

from .database import Base
from sqlalchemy.dialects.mysql import INTEGER, TINYINT  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from typing import Optional



UserRoomCompat = Table(
    "user_room_compat",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("room_id", ForeignKey("rooms.id")),
    UniqueConstraint("user_id", "room_id"),
)


"""RoomEventCompat = Table(
    "room_event_compat",
    Base.metadata,
    Column("room_id", ForeignKey("rooms.id")),
    Column("event_id", ForeignKey("events.id")),
    UniqueConstraint("room_id", "event_id"),
)"""

UserEventParticipation = Table(
    "user_event_participation",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("event_id", ForeignKey("events.id")),
    UniqueConstraint("user_id", "event_id"),
)




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    admin = Column(Boolean, default = False)
    all_rooms = relationship(
        "Room",
        secondary= UserRoomCompat,
        back_populates="users", 
        uselist= True,
    )
    all_events = relationship(
        "Event",
        secondary= UserEventParticipation,
        back_populates="participants", 
        uselist= True,
    )
    


class Recommandation(Base):
    __tablename__ = "recommandations"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    label = Column(String, index=True)
    recommandation_type = Column(String, index=True)
    place = Column(String, index=True)
    availabilites = Column(String, index=True)
    url = Column(String, index=True)
    

    
class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
    invite_link = Column(String, index=True)
    style = Column(String, index=True)
    events = relationship("Event", back_populates="room")

    users = relationship(
        "User",
        secondary= UserRoomCompat,
        back_populates="all_rooms", 
        uselist= True,
    )


 

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
    date = Column(String, index=True)
    place = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(String, index=True)
    room = relationship("Room", back_populates="events")

    participants = relationship(
        "User",
        secondary= UserEventParticipation,
        back_populates="all_events", 
        uselist= True,
    )




class Logs(Base):
    __tablename__ = "logs"

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    user_id: Column[Optional[int]] = Column(ForeignKey("users.id"), index=True)
    timestamp = Column(DateTime)
    action = Column(String(2048))

    user = relationship("User")


