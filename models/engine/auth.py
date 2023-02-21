#!/usr/bin/env python3
"""
    auth module
"""
from models.engine.db import DB, User, Note
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """
        returns salted hash of the input password
    """
    encoded_pass = password.encode('utf-8')
    return hashpw(encoded_pass, gensalt())


def _generate_uuid() -> str:
    """
        generates a new unique string id
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
        """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            takes user's email and password and returns the
            user instance associated with it
        """
        try:
            if self._db.find_obj_by(User, email=email):
                raise ValueError(f"User {email} already exists")
        except Exception:
            pass
        hashed_password = _hash_password(password)
        user = User(email=email, hashed_password=hashed_password.decode('utf-8'))
        self._db.add(user)
        self._db.save()
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
            Checks login details and returns True if info provided
            is correct else it returns False
        """
        try:
            user: User = self._db.find_obj_by(User, email=email)
            return checkpw(password.encode('utf-8'),
                           user.hashed_password.encode('utf-8'))
        except (InvalidRequestError, NoResultFound):
            return False

    def get_user_from_email(self, email: str) -> Union[User, None]:
        """
            takes an email argument and returns the corresponding
            User or None if not found
        """
        try:
            user: User = self._db.find_obj_by(User, email=email)
            return user
        except (InvalidRequestError, NoResultFound):
            return None

    def create_and_save_note(self, user: User, title: str, content: str) -> None:
        """
            takes a user instance and a note string and creates a new
            note associated with the user
        """
        note = Note(title=title, content=content, user_id=user.id)
        self._db.add(note)
        self._db.save()

    def delete_note_by_id(self, user: User, note_id: str) -> None:
        """
            takes a user instance and a note id and deletes the
            corresponding note
        """
        try:
            note: Note = self._db.find_obj_by(Note, id=note_id)
            if note.user_id == user.id:
                self._db.delete(note)
                self._db.save()
        except (InvalidRequestError, NoResultFound):
            pass

    def get_note_by_id(self, user: User, note_id: str) -> Union[Note, None]:
        """
            takes a user instance and a note id and returns the
            corresponding note or None if not found
        """
        try:
            note: Note = self._db.find_obj_by(Note, id=note_id)
            if note.user_id == user.id:
                return note
        except (InvalidRequestError, NoResultFound):
            return None

    def update_and_save_note(self, user: User, note_id: str, title: str,
                             content: str) -> None:
        """
            takes a user instance and a note id and returns the
            corresponding note or None if not found
        """
        try:
            note: Note = self._db.find_obj_by(Note, id=note_id)
            if note.user_id == user.id:
                note.title = title
                note.content = content
                note.updated_at = datetime.utcnow()
                self._db.save()
        except (InvalidRequestError, NoResultFound):
            pass

