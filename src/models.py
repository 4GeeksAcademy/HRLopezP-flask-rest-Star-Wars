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

    def __repr__ (self):
        return self.name

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
    full_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(Enum(GenderEnum), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    height: Mapped[float] = mapped_column(default=0.00)
    url: Mapped[str] = mapped_column(String(150), nullable=False)

# Relación con la tabla Favoritos
    favorite_people: Mapped[List["Favorite"]] = relationship(back_populates="people_item")

    def __repr__ (self):
        return self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "gender": self.gender.value,
            "height": self.height,
            "description": self.description,
            "url": self.url,
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(100), default= "sin información")
    description: Mapped[str] = mapped_column(Text, nullable=False)
    population: Mapped[int] = mapped_column(default=0)
    url: Mapped[str] = mapped_column(String(150), nullable=False)

# Relación con la tabla Favoritos
    favorite_planets: Mapped[List["Favorite"]] = relationship(back_populates="planet_item")

    def __repr__ (self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "description": self.description,
            "url": self.url,
        }


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    model: Mapped[str] = mapped_column(String(100), default= "Sin información")
    capacity: Mapped[int] = mapped_column(default= 0)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(String(150), nullable=False)

# Relación con la tabla Favoritospipenv run reset_db
    favorite_vehicles: Mapped[List["Favorite"]] = relationship(back_populates="vehicle_item")

    def __repr__ (self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "capacity": self.capacity,
            "description": self.description,
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
    
    
    def __repr__(self):
        if self.planet_item is not None:
            return f"Planeta: {self.planet_item.name}"
        elif self.people_item is not None:
            return f"Personaje: {self.people_item.full_name}"
        elif self.vehicle_item is not None:
            return f"Vehículo: {self.vehicle_item.name}"
        return f"Favorito {self.id} - Desconocido"


    def serialize(self):
        data= {
            "id": self.id,
            "user_id": self.user_id,
        }


        if self.planet_id is not None:
            data["type"] = "planet"
            data["details"] = self.planet_item.serialize()
        elif self.people_id is not None:
            data["type"] = "people"
            data["details"] = self.people_item.serialize()
        elif self.vehicle_id is not None:
            data["type"] = "vehicle"
            data["details"] = self.vehicle_item.serialize()
        
        return data
