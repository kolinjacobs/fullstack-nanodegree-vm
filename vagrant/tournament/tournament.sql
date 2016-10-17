-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE players;

CREATE TABLE players
(
id SERIAL,
player_name varchar(255),
wins int,
matches int
);

CREATE TABLE matches
(
id_one int,
player_one varchar(255),
id_two int,
player_two varchar(255),
winner int
);