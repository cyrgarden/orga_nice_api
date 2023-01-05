from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float,Table, UniqueConstraint
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    admin = Column(TINYINT(1))

    items = relationship("Item", back_populates="owner")
    rooms = relationship(
        "Room",
        secondary = UserRoomCompat,
        back_populates="users",
        uselist=True,
    )


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Recommandation(Base):
    __tablename__ = "recommandations"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    label = Column(String, index=True)
    recommandation_type = Column(String, index=True)
    place = Column(String, index=True)
    availabilites = Column(String, index=True)
    
class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
    invite_link = Column(String, index=True)
    style = Column(String, index=True)

    users = relationship(
        "User",
        secondary= UserRoomCompat,
        back_populates="all_rooms", 
        uselist= True,
    )

class Logs(Base):
    __tablename__ = "logs"

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    user_id: Column[Optional[int]] = Column(ForeignKey("users.id"), index=True)
    timestamp = Column(DateTime)
    action = Column(String(2048))

    user = relationship("User")


