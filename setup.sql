DROP DATABASE IF EXISTS rssBot;

CREATE DATABASE rssBot
    DEFAULT CHARSET utf8 COLLATE = utf8_general_ci;

use rssBot;

CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT NOT NULL,
    chat_id BIGINT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS urls(
    id INT AUTO_INCREMENT NOT NULL,
    title TEXT(2048) NOT NULL,
    url TEXT(2048) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS user_url(
    id INT AUTO_INCREMENT NOT NULL,
    user_id INT NOT NULL,
    url_id INT NOT NULL,
    tags TEXT(2048),
    PRIMARY KEY(id)
);
ALTER TABLE user_url ADD
    FOREIGN KEY(user_id)
    REFERENCES users(id);
ALTER TABLE user_url ADD
    FOREIGN KEY(url_id)
    REFERENCES urls(id);

CREATE TABLE IF NOT EXISTS config(
    id INT AUTO_INCREMENT NOT NULL,
    chat_id BIGINT NOT NULL,
    max_news INT NOT NULL DEFAULT 5,
    last_update INT,
    timer TINYINT NOT NULL DEFAULT 24,
    first_send TINYINT NOT NULL DEFAULT 8,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS sessions(
    user_id BIGINT NOT NULL,
    control_id BIGINT NOT NULL,
    started INT NOT NULL
);

commit;