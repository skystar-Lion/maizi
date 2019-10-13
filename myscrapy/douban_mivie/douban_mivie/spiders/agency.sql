USE 12306_site;

CREATE TABLE scrapy_agency (
  province varchar(5) NOT NULL,
  city varchar(5) NOT NULL,
  country varchar(5) NOT NULL,
  agency_name varchar(30) NOT NULL,
  address varchar(40) NOT NULL,
  start_time varchar(5) NOT NULL,
  end_time varchar(5) NOT NULL,
  windows_quality tinyint(4) NOT NULL,
  PRIMARY KEY (address)
) engine = innodb, charset = utf8;

