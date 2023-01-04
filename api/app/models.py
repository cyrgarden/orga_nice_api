from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float,Table
from sqlalchemy.orm import relationship

from .database import Base


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
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    rooms = relationship(
        "Room",
        secondary = UserRoomCompat,
        back_populates="users"
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
