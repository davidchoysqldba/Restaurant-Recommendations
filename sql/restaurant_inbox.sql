CREATE TABLE `restaurant_inbox` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(400) NOT NULL,
  `rest_desc_json` varchar(5000) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `virtual_inspection_date` datetime GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.inspection_date')) VIRTUAL,
  `virtual_zipcode` varchar(5) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.zipcode')) VIRTUAL,
  `virtual_cuisine` varchar(200) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.cuisine_description')) VIRTUAL,
  `virtual_boro` varchar(20) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.boro')) VIRTUAL,
  `virtual_grade_date` datetime GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.grade_date')) VIRTUAL,
  `virtual_grade` varchar(10) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.grade')) VIRTUAL,
  `virtual_camis` varchar(20) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.camis')) VIRTUAL,
  `virtual_dba` varchar(200) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.dba')) VIRTUAL,
  PRIMARY KEY (`id`),
  KEY `idx_restaurant_inbox_virtual_inspection_date` (`virtual_inspection_date`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`rest_desc_json` is null or json_valid(`rest_desc_json`))
) ENGINE=InnoDB AUTO_INCREMENT=773502 DEFAULT CHARSET=latin1