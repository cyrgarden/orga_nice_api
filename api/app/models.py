from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float,Table, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship

from .database import Base
from sqlalchemy.dialects.mysql import INTEGER, TINYINT  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from typing import Optional




"""UserIndispo = Table(
    "user_indispo",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("indispo_id",ForeignKey("indisponibilities.id")),
    UniqueConstraint("user_id", "indispo_id"),
)

RoomIndispo = Table(
    "room_indispo",
    Base.metadata,
    Column("room_id", ForeignKey("rooms.id")),
    Column("indispo_id",ForeignKey("indisponibilities.id")),
    UniqueConstraint("room_id", "indispo_id"),
)"""

UserRoomCompat = Table(
    "user_room_compat",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("room_id", ForeignKey("rooms.id")),
    UniqueConstraint("user_id", "room_id"),
)


UserEventParticipation = Table(
    "user_event_participation",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("event_id", ForeignKey("events.id")),
    UniqueConstraint("user_id", "event_id"),
)


UserTaskAssignation = Table(
    "user_task_assignation",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("task_id", ForeignKey("tasks.id")),
    UniqueConstraint("user_id", "task_id"),
)



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True)
    mail = Column(String(255), unique=True)
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
    
    all_tasks = relationship(
        "Task",
        secondary= UserTaskAssignation,
        back_populates="owners", 
        uselist= True,
    )
    
    all_indisponibitilies = relationship("Indisponibility", back_populates="user")


class Recommandation(Base):
    __tablename__ = "recommandations"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    label = Column(String, index=True)
    recommandation_type = Column(String, index=True)
    subtype = Column(String, index= True)
    place = Column(String, index=True)
    availabilites = Column(String, index=True)
    url = Column(String, index=True)
    lat = Column(Float)
    lon = Column(Float)



class Indisponibility(Base):
    __tablename__ ='indisponibilities'
    
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="all_indisponibitilies")
    
    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("Room", back_populates="all_indisponibitilies")
    
    
class PendingPassword(Base):
    __tablename__ = "pending_passwords"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Float)
    new_password = Column(String)
    

    
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
    
    all_indisponibitilies = relationship("Indisponibility", back_populates="room")


 

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(String, index=True)
    place = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(String, index=True)

    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("Room", back_populates="events")
    
    associated_tasks = relationship("Task", back_populates="event")


    participants = relationship(
        "User",
        secondary= UserEventParticipation,
        back_populates="all_events", 
        uselist= True,
    )




class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    completed = Column(Boolean, index=True)
    description = Column(String, index=True)
    
    event_id = Column(Integer, ForeignKey("events.id"))
    event = relationship("Event", back_populates="associated_tasks")
    
    
    owners = relationship(
        "User",
        secondary= UserTaskAssignation,
        back_populates="all_tasks", 
        uselist= True,
    )
    
class Logs(Base):
    __tablename__ = "logs"

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    user_id: Column[Optional[int]] = Column(ForeignKey("users.id"), index=True)
    timestamp = Column(DateTime)
    action = Column(String(2048))

    user = relationship("User")


