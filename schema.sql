create database notes;


create table accounts (
    id SERIAL primary key,
    email varchar(40),
    password varchar(20),
    user_id int
);

create table notes (
    id SERIAL primary key,
    subject varchar,
    content text,
    user_id int
);