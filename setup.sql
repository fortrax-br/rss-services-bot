CREATE DATABASE IF NOT EXISTS rssBot
    DEFAULT CHARSET utf8 COLLATE = utf8_general_ci;


CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT NOT NULL,
    chat_id BIGINT NOT NULL,
    PRIMARY KEY(id)
);


CREATE TABLE IF NOT EXISTS sessions(
    user_id INT NOT NULL,
    control_id INT NOT NULL,
    started INT NOT NULL
);
ALTER TABLE sessions ADD CONSTRAINT fk_sessions_user
    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE no action
    ON UPDATE no action;
ALTER TABLE sessions ADD CONSTRAINT fk_sessions_control
    FOREIGN KEY(control_id)
    REFERENCES users(id)
    ON DELETE no action
    ON UPDATE no action;

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
ALTER TABLE user_url ADD CONSTRAINT fk_user
    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE no action
    ON UPDATE no action;
ALTER TABLE user_url ADD CONSTRAINT fk_url
    FOREIGN KEY(url_id)
    REFERENCES urls(id)
    ON DELETE no action
    ON UPDATE no action;


CREATE TABLE IF NOT EXISTS config(
    id INT AUTO_INCREMENT NOT NULL,
    user_id INT NOT NULL,
    max_news INT NOT NULL DEFAULT 5,
    last_update INT,
    timer TINYINT NOT NULL DEFAULT 24,
    start TINYINT NOT NULL DEFAULT 8,
    PRIMARY KEY(id)
);
ALTER TABLE config ADD CONSTRAINT fk_config
    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE no action
    ON UPDATE no action;

commit;