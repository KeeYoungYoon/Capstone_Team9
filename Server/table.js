create database projdb;
use projdb;

create table raspdata (
id int not null auto_increment primary key,
speed decimal(4,1) unsigned,
acceleration decimal(5,1) signed,
light_type char(1),
time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
