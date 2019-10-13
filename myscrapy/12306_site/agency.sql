drop table ticket_agency;

create table ticket_agency(
id int primary key auto_increment,
province varchar(5) not null,
city varchar(5) not null,
country varchar(5) not null,
agency_name varchar(30) not null,
address varchar(40) not null,
start_time varchar(5) not null,
end_time varchar(5) not null,
windows_quality varchar(1) not null
)engine = innodb, charset = utf-8;



