#!/usr/bin/env python3
"""
    db module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from models.user import User
from models.basemodel import Base
from models.notes import Note

from os import getenv


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        env = getenv("NOTE_ENV", None)
        user = getenv("NOTE_USER", None)
        password = getenv("NOTE_PASSWD", None)
        host = getenv("NOTE_HOST", None)
        database = getenv("NOTE_DB", None)

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                user, password, host, database
            ),
            echo=False,
        )
        self.__session = None

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            Base.metadata.create_all(self.__engine)
            sess_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False
            )
            Session = scoped_session(sess_factory)
            self.__session = Session
        return self.__session

    def save(self) -> None:
        """Save the current session"""
        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e

    def add(self, obj) -> None:
        """Add an object to the current session"""
        self._session.add(obj)

    def find_obj_by(self, cls, **kwargs) -> object:
        """Find an object by a given key/value pair"""
        if cls and kwargs:
            if type(cls) is str:
                cls = eval(cls)
            for key in kwargs:
                if key not in cls.__dict__:
                    raise InvalidRequestError
            obj = self._session.query(cls).filter_by(**kwargs).first()
            if obj is not None:
                return obj
            raise NoResultFound
        raise InvalidRequestError

    def find_obj_all_by(self, cls, **kwargs) -> object:
        """Find an object by a given key/value pair"""
        if cls and kwargs:
            if type(cls) is str:
                cls = eval(cls)
            for key in kwargs:
                if key not in cls.__dict__:
                    raise InvalidRequestError
            obj = self._session.query(cls).filter_by(**kwargs).all()
            if obj is not None:
                return obj
            raise NoResultFound
        raise InvalidRequestError

    def reload(self) -> None:
        """Reload the current session"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def delete(self, obj) -> None:
        """Delete an object from the current session"""
        self._session.delete(obj)

    def close(self) -> None:
        """Close the current session"""
        self._session.close()
