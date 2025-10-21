from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import enum
from datetime import datetime, UTC

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    upgrade: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relación con la tabla Favoritos
    favorites_item: Mapped[List["Favorite"]] = relationship(back_populates="user_item")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "subscription_date": str(self.subscription_date),
            "upgrade": self.upgrade,
        }


class GenderEnum(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(Enum(GenderEnum), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    height: Mapped[float] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(String(150), nullable=False)

# Relación con la tabla Favoritos
    favorite_people: Mapped[List["Favorite"]] = relationship(back_populates="people_item")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "gender": self.gender.value,
            "height": self.height,
            "url": self.url,
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(150), nullable=False)
    population: Mapped[int] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(String(150), nullable=False)

# Relación con la tabla Favoritos
    favorite_planets: Mapped[List["Favorite"]] = relationship(back_populates="planet_item")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "url": self.url,
        }


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=True)
    capacity: Mapped[int] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(String(150), nullable=False)

# Relación con la tabla Favoritos
    favorite_vehicles: Mapped[List["Favorite"]] = relationship(back_populates="vehicle_item")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "capacity": self.capacity,
            "url": self.url,
        }


class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    # Creación del foreignkey
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(db.ForeignKey("planet.id"), nullable=True) 
    people_id: Mapped[int] = mapped_column(db.ForeignKey("people.id"), nullable=True) 
    vehicle_id: Mapped[int] = mapped_column(db.ForeignKey("vehicle.id"), nullable=True) 

    # Relaciones con otras tablas
    user_item: Mapped["User"] = relationship(back_populates="favorites_item")
    planet_item: Mapped["Planet"] = relationship(back_populates="favorite_planets")
    people_item: Mapped["People"] = relationship(back_populates="favorite_people")
    vehicle_item: Mapped["Vehicle"] = relationship(back_populates="favorite_vehicles")
    

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }
