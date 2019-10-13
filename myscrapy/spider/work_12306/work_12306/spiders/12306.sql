CREATE DATABASE 12306_site;

CREATE TABLE `station_info` (
  `train_bureau` varchar(10) NOT NULL,
  `station_type` char(1) NOT NULL,
  `station_name` varchar(20) NOT NULL,
  `station_address` varchar(100) NOT NULL,
  `passengers` varchar(5) NOT NULL,
  `luggage` varchar(5) NOT NULL,
  `package` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8；


CREATE TABLE `station_time` (
  `date` date NOT NULL,
  `train_code` varchar(5) NOT NULL,
  `station_no` varchar(2) NOT NULL,
  `station_name` varchar(10) NOT NULL,
  `START_TIME` varchar(10) NOT NULL,
  `ARRIVE_TIME` varchar(10) NOT NULL,
  `stopover_time` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8；

CREATE TABLE `station_agency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `province` varchar(10) NOT NULL,
  `city` varchar(10) NOT NULL,
  `county` varchar(150) NOT NULL,
  `agency_name` varchar(50) NOT NULL,
  `agency_address` varchar(50) NOT NULL,
  `start_time_am` varchar(5) NOT NULL,
  `stop_time_pm` varchar(5) NOT NULL,
  `windows_quantity` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8；

CREATE TABLE `station_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `station_name` varchar(10) NOT NULL,
  `station_code` varchar(5) NOT NULL,
  PRIMARY KEY (`id`,`station_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8；


CREATE TABLE `station_ticket` (
  `train_code` varchar(5) NOT NULL,
  `start_station` varchar(10) NOT NULL,
  `to_station` varchar(10) NOT NULL,
  `swz_num` varchar(3) NOT NULL,
  `tz_num` varchar(3) NOT NULL,
  `zy_num` varchar(3) NOT NULL,
  `ze_num` varchar(3) NOT NULL,
  `gr_num` varchar(3) NOT NULL,
  `rw_num` varchar(3) NOT NULL,
  `yw_num` varchar(3) NOT NULL,
  `rz_num` varchar(3) NOT NULL,
  `yz_num` varchar(3) NOT NULL,
  `wz_num` varchar(3) NOT NULL,
  `qt_num` varchar(3) NOT NULL,
  PRIMARY KEY (`train_code`,`start_station`,`to_station`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8；


CREATE TABLE `train_info` (
  `date` date NOT NULL,
  `train_code` varchar(5) NOT NULL,
  `train_num` varchar(20) NOT NULL,
  `start_station` varchar(10) NOT NULL,
  `to_station` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8；