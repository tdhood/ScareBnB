"""SQLAlchemy models for ScareBnB."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import jwt

load_dotenv()

secret_key = os.environ["SECRET_KEY"]
bcrypt = Bcrypt()
db = SQLAlchemy()

# DEFAULT_HOUSE_IMAGE_URL = (
#     "https://scare-bnb.sfo2.digitaloceanspaces.com/horror-flick-abandoned-home.jpg"
# )


class User(db.Model):
    """User in the system."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )

    last_name = db.Column(db.Text, nullable=False)

    # image_url = db.Column(
    #     db.Text,
    #     default=DEFAULT_IMAGE_URL,
    # )

    bio = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    is_host = db.Column(
        db.Boolean,
        nullable=False,
    )

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bio": self.bio,
            "is_host": self.is_host,
        }

    @classmethod
    def signup(
        cls, username, email, password, first_name, last_name, bio, is_host=False
    ):
        """Sign up user.

        Hashes password and adds user to system.
        """
        print("password", password)
        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")
        print("hashed", hashed_pwd)
        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
            is_host=is_host,
        )
        token = jwt.encode({"username": username}, secret_key)

        db.session.add(user)
        return [user, token]

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).one_or_none()
        print('do i find guest?', user)

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                token = jwt.encode({"username": username}, secret_key)
                return [user, token]

        return False

    @classmethod
    def create_token(cls, username):
        """Create token for user"""
        print("create_token")
        print("secret key", secret_key)
        token = jwt({"username": username}, secret_key)
        return token


class Listing(db.Model):
    """An individual property listings."""

    __tablename__ = "listings"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    title = db.Column(
        db.String(20),
        nullable=False,
    )
    object_name = db.Column(
        db.Text,
        nullable=False,
    )

    location = db.Column(
        db.String(20),
        nullable=False,
    )

    description = db.Column(
        db.String(500),
        nullable=False,
    )

    price = db.Column(
        db.Integer,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
    )

    host_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    rating = db.Column(
        db.Integer,
        nullable=False,
    )

    def __repr__(self):
        return (
            f"<Listing #{self.id}: title: {self.title}, object_name: {self.object_name}"
        )

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "object_name": self.object_name,
            "host": self.host_id,
            "price": self.price,
            "image_url": self.image_url,
            "rating": self.rating,
        }


class Favorite(db.Model):
    """Favorite listings for a user"""

    __tablename__ = "favorites"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("listing.id", ondelete="CASCADE"),
        nullable=False,
    )

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "id": self.id,
            "user": self.user_id,
            "listing": self.listing_id,
        }

    



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


