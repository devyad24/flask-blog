DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS child;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT,
    parent_type TEXT CHECK(parent_type in ('FirstTime', 'Experienced')) NOT NULL DEFAULT 'FirstTime'

);

CREATE TABLE child (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT NOT NULL,
    lastname TEXT,
    age INT CHECK(age > 0 and age < 14) NOT NULL,
    gender TEXT CHECK(gender in ('Male', 'Female')) NOT NULL,
    parent_id INTEGER NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES user (id)
);

-- CREATE TABLE relationship (
--     guardian INTEGER NOT NULL,
--     kid INTEGER NOT NULL

-- )

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)
);