# TODO: populate with location and user starter data

import sqlite3
from app import 
from models import Listing, User

conn = sqlite3.connect('scarebnb.db')
cur = conn.cursor()

cur.executescript("""
    BEGIN;
    CREATE TABLE users ( 
        id SERIAL PRIMARY KEY,
        email TEXT NOT NULL
            CHECK (position('@' IN email) > 1),
        username TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        bio TEXT,
    password TEXT NOT NULL,
    is_host BOOLEAN NOT NULL DEFAULT FALSE
    );
    COMMIT:
""")

cur.executescript("""
    BEGIN;
    CREATE TABLE listings (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        object_name TEXT NOT NULL,
        location TEXT NOT NULL,
        description TEXT NOT NULL,
        price INTEGER NOT NULL,
        image_url TEXT NOT NULL,
        rating INTEGER NOT NULL,
        user_id INTEGER NOT NULL
            REFERENCES users ON DELETE CASCADE
    );
    COMMIT;
""")


cur.execute("DROP DATABASE scarebnb")

u1 = User(
            username="testuser",
            password='password',
            email="user@email.com",
            first_name='First',
            last_name='Last',
            bio='bio is here',
            is_host=True,
)
db.session.add_all([u1])
db.session.commit()

l1 = Listing(
            title="Hauntingly Isolated",
            object_name='lakehouse',
            description="Remote",
            location="The lake",
            price=200,
            user_id=1,
            rating=5,
            image_url="https://kestrelbucket.s3.amazonaws.com/scarebnb/lakehouse.jpg"
        )

db.session.add_all([l1])
db.session.commit()