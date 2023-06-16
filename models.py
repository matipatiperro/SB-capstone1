"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    password = db.Column(
        db.Text,
        nullable=False,
    )

    playlists = db.relationship('Playlist', backref="user")

    @classmethod
    def signup(cls, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

class Playlist(db.Model):
    """playlists"""

    __tablename__ = "playlists"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(30),
                     nullable=False,
                     unique=False)
    description = db.Column(db.String(75),
                    nullable=True,
                    unique=False)

    songs = db.relationship('Song', backref="playlists")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Song(db.Model):
    """songs to playlist"""

    __tablename__ = "songs"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    artist = db.Column(db.String(30),
                     nullable=False,
                     unique=False)
    title = db.Column(db.String(50),
                    nullable=True,
                    unique=False)
    notes = db.Column(db.String(75),
                    nullable=True,
                    unique=False)

    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)