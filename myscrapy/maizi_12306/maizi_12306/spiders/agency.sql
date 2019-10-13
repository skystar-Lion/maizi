USE 12306_site;

CRETAE TABLE scrapy_agency(
  `province` varchar(10) NOT NULL,
  `city` varchar(10) NOT NULL,
  `country` varchar(10) NOT NULL,
  `agency_name` varchar(30) NOT NULL,
  `address` varchar(40) NOT NULL,
  `start_time` varchar(5) NOT NULL,
  `end_time` varchar(5) NOT NULL,
  `windows_quality` tinyint(4) NOT NULL,
  PRIMARY KEY (`address`)
);

