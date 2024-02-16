#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from os import getenv


class DBStorage:
    """This class manages storage of hbnb models from and to database"""
    __engine = None
    __session = None

    def __init__(self):
        """Constructor"""

        # set up engine
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            user, passwd, host, db
        ), pool_pre_ping=True)

        # drop all tables
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
           Get all object of a class from database,
           if cls=None, Will return all objects of all classes
        """
        def get_objects(cls):
            """Helper function that gets all object from a class"""
            objects = self.__session.query(cls).all()
            instances = {}

            for obj in objects:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                instances[key] = obj

            return instances

        instances = {}
        if cls:
            cls = eval(cls)
            instances = get_objects(cls)
        else:
            classes = [City, Place, User,
                       Amenity, Review, State]
            for cls in classes:
                instances.update(get_objects(cls))

        return instances

    def new(self, obj):
        """
            Adds the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        # create all tables in the database
        Base.metadata.create_all(self.__engine)

        # Create a session
        session_factory = sessionmaker(self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """calls remove() method on the private session attribute"""
        self.__session.remove()
