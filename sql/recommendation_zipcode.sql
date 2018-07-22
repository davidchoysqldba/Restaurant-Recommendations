CREATE TABLE `recommendation_zipcode` (
  `recommendation_id` int(11) NOT NULL AUTO_INCREMENT,
  `zipcode` varchar(10) DEFAULT NULL,
  `boro` varchar(20) DEFAULT NULL,
  `dba` varchar(200) DEFAULT NULL,
  `grade_average` float(7,2) DEFAULT NULL,
  `grade_count` float(7,2) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `is_latest` bit(1) DEFAULT NULL,
  PRIMARY KEY (`recommendation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1865 DEFAULT CHARSET=latin1