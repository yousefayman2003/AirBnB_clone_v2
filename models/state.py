#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref
from models.base_model import BaseModel, Base


class State(BaseModel):
    """ State class """
    __tablename__ = "states"
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all, delete-orphan",
                              backref=backref("state", cascade="all"),
                              single_parent=True)

    else:
        @property
        def cities(self):
            """returns the list of City instances with state_id equals to the current State.id"""
            from models import storage
            from models.city import City

            instances = storage.all(City)

            return [city for city in instances.values() if self.id == city.state_id]
