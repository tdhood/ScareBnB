CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL
    CHECK (email LIKE '%@%' AND email NOT LIKE '@%'),
  username TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  bio TEXT,
  password TEXT NOT NULL,
  is_host BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE listings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  object_name TEXT NOT NULL,
  location TEXT NOT NULL,
  description TEXT NOT NULL,
  price INTEGER NOT NULL,
  image_url TEXT NOT NULL,
  rating INTEGER NOT NULL,
  host_id INTEGER NOT NULL
    REFERENCES users ON DELETE CASCADE
);