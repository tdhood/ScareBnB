
INSERT INTO users (email, username, first_name, last_name, bio, password, is_host)
VALUES ('guest@email.com',
        'guest',
        'guest',
        'guest',
        'guest',
        '$2b$12$tTB1ldJuYMFMXhCUEwnjqOk9107UzmSxU7/HhCeJncGSJRbMyIwGi',
        FALSE),
        ('user@email.com',
        'testuser',
        'Test',
        'User',
        'test bio',
        '$2b$12$iEyKMChClC4VuCo1FSRtReIuaNMA59guYXN3yK0o.eG3ZX4NKnZOy',
        FALSE),
       ('host@host.com',
        'hostuser',
        'Host',
        'User2',
        'test bio2',
        '$2b$12$AZH7virni5jlTTiGgEg4zu3lSvAw68qVEfSIOjJ3RqtbJbdW/Oi5q',
        TRUE);

INSERT INTO listings (title, object_name, location, description, price, image_url, rating, host_id)
VALUES('Hauntingly Isolated',
        'lakehouse',
        'Remote',
    'No one can hear you scream',
    200,
    'https://st3.depositphotos.com/4035913/13242/i/450/depositphotos_132427622-stock-illustration-haunted-spooky-house.jpg',
    5,
    3);


