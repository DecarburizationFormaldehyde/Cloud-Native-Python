CREATE TABLE apirelease(
    buildtime date,
    version varchar(30) primary key ,
    links varchar2(30),methods varchar2(30)
);
INSERT into apirelease values('2017-01-01 10:00:00','v1','/api/v1/users','get, post, put, delete');

CREATE TABLE users(
    username varchar2(30),
    emailid varchar2(30),
    password varchar2(30),
    id integer primary key autoincrement
);

ALTER TABLE users
ADD full_name varchar2(30);

INSERT INTO  users
(username, emailid, password,full_name)
values (
        'Manish',
        'manish@gmail.com',
        'manish123',
        'Manish John'
       );

CREATE TABLE tweets(
    id integer primary key autoincrement ,
    username varchar2(30),
    body varchar2(30),
    tweet_time date
);

INSERT INTO tweets
(username, body, tweet_time)
values (
        'Manish',
        'Hello World',
        '2017-01-01 10:00:00'
       );