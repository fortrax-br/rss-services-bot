CREATE TABLE users(
    id INT AUTO_INCREMENT NOT NULL,
    chat_id BIGINT NOT NULL,
    PRIMARY KEY(id)
);


CREATE TABLE urls(
    id INT AUTO_INCREMENT NOT NULL,
    title TEXT(2048) NOT NULL,
    url TEXT(2048) NOT NULL,
    PRIMARY KEY(id)
);


CREATE TABLE user_url(
    id INT AUTO_INCREMENT NOT NULL,
    user_id INT NOT NULL,
    url_id INT NOT NULL,
    tags TEXT(2048),
    last_update TEXT,
    max_news INT DEFAULT NULL,
    PRIMARY KEY(id)
);
ALTER TABLE user_url ADD
    FOREIGN KEY(user_id)
    REFERENCES users(id);
ALTER TABLE user_url ADD
    FOREIGN KEY(url_id)
    REFERENCES urls(id);


CREATE TABLE timers(
    id INT NOT NULL AUTO_INCREMENT,
    chat_id BIGINT NOT NULL,
    timer VARCHAR(5) NOT NULL,
    PRIMARY KEY(id)
);


CREATE TABLE config(
    id INT AUTO_INCREMENT NOT NULL,
    chat_id BIGINT NOT NULL,
    max_news INT NOT NULL DEFAULT 5,
    PRIMARY KEY(id)
);


CREATE TABLE sessions(
    chat_id BIGINT NOT NULL,
    control_id BIGINT NOT NULL,
    started INT NOT NULL
);

commit;
