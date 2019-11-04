create database if not exists chatapp;
create table user;

create table if not exists user(userid int(11), username varchar(100), password varchar(100), primary key (userid));

insert into user values(1, 'user1', '123');

insert into user values(2, 'user2', 'qwerty');
