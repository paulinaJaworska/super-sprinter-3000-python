DROP TABLE IF EXISTS users;

CREATE TABLE users (
                       id serial NOT NULL,
                       username varchar(250)  NOT NULL UNIQUE ,
                       password varchar(250)  NOT NULL

);

ALTER TABLE ONLY users ADD CONSTRAINT pk_users_id PRIMARY KEY (id);
-- ONLY - only this table will be alter (and not the ones that this table reference)