use FORMULA_1;
CREATE table apis(
id int primary key auto_increment,
nombre varchar(100) not null unique,
url varchar(1000),
control_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
ON UPDATE CURRENT_TIMESTAMP
)AUTO_INCREMENT=1;


insert into apis(nombre,url) values ("ergast","https://ergast.com/mrd/"),("rapid-api-formula-1","https://rapidapi.com/api-sports/api/api-formula-1");

create table grand_prix(
id int primary key auto_increment,
`name` varchar(300) not null unique,
country varchar(200),
`url` varchar(1000),
primer_gp date,
id_api_formula_1 int,
control_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
ON UPDATE CURRENT_TIMESTAMP
)auto_increment=1;

create table circuits(
id int primary key auto_increment,
`name` varchar(300) not null unique,
country varchar(200),
city varchar(200),
`lat` varchar(100),
`long` varchar(100),
laps int,
`legth` varchar(100),
race_distance varchar(400),
capacity int,
opened int,
first_grand_prix int,
id_api_postman varchar(100),
id_api_formula_1 int,
`url` varchar(1000),
control_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
ON UPDATE CURRENT_TIMESTAMP
)auto_increment=1;


create table seasons(
season int unsigned primary key,
url varchar(1000),
control_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
ON UPDATE CURRENT_TIMESTAMP
);










create table calendario(
id int primary key auto_increment,
`id_circuit` int,
id_gp int,
season int unsigned,
round int,
laps int,
`fecha` datetime,
`status` varchar(200),
weather varchar(100),
`url` varchar(1000),
id_api_formula_1 int,
fecha_3rdQualifying datetime,
weather_3rdQualifying varchar(200),
id_api_formula_3rdQualifying int,

fecha_2ndQualifying datetime,
weather_2ndQualifying varchar(200),
id_api_formula_2ndQualifying int,

fecha_1stQualifying datetime,
weather_1stQualifying varchar(200),
id_api_formula_1stQualifying int,

fecha_3rdPractice datetime,
weather_3rdPractice varchar(200),
id_api_formula_3rdPractice int,

fecha_2ndPractice datetime,
weather_2ndPractice varchar(200),
id_api_formula_2ndPractice int,

fecha_1stPractice datetime,
weather_1stPractice varchar(200),
id_api_formula_1stPractice int,

fecha_Sprint datetime,
weather_Sprint varchar(200),
id_api_formula_Sprint int,
control_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT FK_calendario_season
    FOREIGN KEY (season)
      REFERENCES seasons(season),
  CONSTRAINT FK_calendario_id_circuito
    FOREIGN KEY (id_circuit)
      REFERENCES circuits(id),
  CONSTRAINT FK_calendario_id_gran_prix
    FOREIGN KEY (id_gp)
      REFERENCES grand_prix(id)
)auto_increment=1;




