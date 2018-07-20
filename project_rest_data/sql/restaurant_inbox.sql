/*

alter table restaurant_inbox
add date_created DATETIME, 
add date_mofied DATETIME;
-- 18.939 sec


alter table restaurant_inbox
change column date_mofied date_modified DATETIME;

*/

select count(*) from restaurant_inbox; # 344186 rows 02/04/2018


/*

select 
#STR_TO_DATE(substring_index(substring_index(file_name, '_', -3), '.', 1), '%Y_%m_%d') as file_name,
* 
from restaurant_inbox;


select 
--file_name = right(file_name, 15),
* from restaurant_inbox
-- where date_created is null
-- 1000 rows 000.27 sec


update restaurant_inbox
set 
date_created = STR_TO_DATE(substring_index(substring_index(file_name, '_', -3), '.', 1), '%Y_%m_%d'),
date_modified = STR_TO_DATE(substring_index(substring_index(file_name, '_', -3), '.', 1), '%Y_%m_%d')
where date_created is null;
24.808 sec
341181 rows

*/




alter table restaurant_inbox add virtual_inspection_date datetime as (json_value(rest_desc_json, '$.inspection_date'));

desc restaurant_inbox

+-------------------------+---------------+------+-----+---------+-------------------+
| Field                   | Type          | Null | Key | Default | Extra             |
+-------------------------+---------------+------+-----+---------+-------------------+
| id                      | int(11)       | NO   | PRI | NULL    | auto_increment    |
| file_name               | varchar(400)  | NO   |     | NULL    |                   |
| rest_desc_json          | varchar(5000) | YES  |     | NULL    |                   |
| date_created            | datetime      | YES  |     | NULL    |                   |
| date_modified           | datetime      | YES  |     | NULL    |                   |
| virtual_inspection_date | datetime      | YES  |     | NULL    | VIRTUAL GENERATED |
+-------------------------+---------------+------+-----+---------+-------------------+



/*

SELECT 
    ->      table_schema as `Database`, 
    ->      table_name AS `Table`, 
    ->      round(((data_length + index_length) / 1024 / 1024), 2) `Size in MB` 
    -> FROM information_schema.TABLES 
    -> ORDER BY (data_length + index_length) DESC;
+--------------------+----------------------------------------------------+------------+
| Database           | Table                                              | Size in MB |
+--------------------+----------------------------------------------------+------------+
| restaurantdb       | restaurant_inbox                                   | 298.77     |
| mysql              | help_topic                                         | 0.45       |
| mysql              | help_keyword                                       | 0.10       |
| mysql              | help_relation                                      | 0.03       |
| information_schema | PLUGINS                                            | 0.02       |
| information_schema | PROCESSLIST                                        | 0.02       |
| information_schema | PARTITIONS                                         | 0.02       |
| information_schema | VIEWS                                              | 0.02       |
| information_schema | PARAMETERS                                         | 0.02       |
| information_schema | COLUMNS                                            | 0.02       |
| information_schema | TRIGGERS                                           | 0.02       |
| information_schema | EVENTS                                             | 0.02       |
| information_schema | ALL_PLUGINS                                        | 0.02       |
| information_schema | SYSTEM_VARIABLES                                   | 0.02       |
| information_schema | ROUTINES                                           | 0.02       |
| mysql              | db                                                 | 0.01       |
| mysql              | proxies_priv                                       | 0.01       |

+--------------------+----------------------------------------------------+------------+


|  95 | restaurant_data_2016_09_06.json | {"action":"Violations were cited in the following area(s).","boro":"QUEENS","building":"11304","camis":41681367,"critical_flag":"Critical","cuisine_description":"Chinese","dba":"JUMBO CHINESE KITCHEN","grade":null,"grade_date":null,"inspection_date":"2016-09-06T00:00:00.000","inspection_type":"Cycle Inspection \/ Initial Inspection","phone":"7184415946","record_date":"2018-01-03T06:00:54.000","score":30.0,"street":"JAMAICA AVENUE","violation_code":"02G","violation_description":"Cold food item held above 41\u00c2\u00ba F (smoked fish and reduced oxygen packaged foods above 38 \u00c2\u00baF) except during necessary preparation.","zipcode":11418}


*/



alter table restaurant_inbox drop virtual_grade_date;
alter table restaurant_inbox drop virtual_boro;
alter table restaurant_inbox drop virtual_zipcode;
alter table restaurant_inbox drop virtual_cuisine;
alter table restaurant_inbox drop virtual_cuisine_description;

alter table restaurant_inbox add virtual_grade_date datetime as (json_value(rest_desc_json, '$.grade_date'));

alter table restaurant_inbox add virtual_boro varchar(20) as (json_value(rest_desc_json, '$.boro'));

alter table restaurant_inbox add virtual_zipcode varchar(5) as (json_value(rest_desc_json, '$.zipcode'));

alter table restaurant_inbox add virtual_cuisine varchar(200) as (json_value(rest_desc_json, '$.cuisine_description'));

alter table restaurant_inbox add virtual_grade varchar(200) as (json_value(rest_desc_json, '$.grade'));

select virtual_grade_date, virtual_boro, virtual_zipcode from restaurant_inbox;
--2.5 sec


explain select virtual_grade_date, virtual_boro, virtual_zipcode from restaurant_inbox;
+------+-------------+------------------+------+---------------+------+---------+------+--------+-------+
| id   | select_type | table            | type | possible_keys | key  | key_len | ref  | rows   | Extra |
+------+-------------+------------------+------+---------------+------+---------+------+--------+-------+
|    1 | SIMPLE      | restaurant_inbox | ALL  | NULL          | NULL | NULL    | NULL | 347571 |       |
+------+-------------+------------------+------+---------------+------+---------+------+--------+-------+



select virtual_grade_date, virtual_boro, virtual_zipcode, virtual_cuisine from restaurant_inbox;
345643 rows in set (3.02 sec)


select distinct virtual_grade_date, virtual_boro, virtual_zipcode, virtual_cuisine from restaurant_inbox;
70239 rows in set (3.75 sec)


alter table restaurant_inbox drop column virtual_grade_date;

alter table restaurant_inbox add virtual_grade_date date as ifnull(json_value(rest_desc_json, '$.grade_date'), NULL);

show binary logs;
+--------------------+-----------+
| Log_name           | File_size |
+--------------------+-----------+
| master1-bin.000002 |   1110402 |
+--------------------+-----------+
1 row in set (0.02 sec)



/*

-- DLL so far! --
CREATE TABLE `restaurant_inbox` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(400) NOT NULL,
  `rest_desc_json` varchar(5000) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `virtual_inspection_date` datetime GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.inspection_date')) VIRTUAL,
  `virtual_cuisine_description` datetime GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.cuisine_description')) VIRTUAL,
  `virtual_grade_date` datetime GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.grade_date')) VIRTUAL,
  `virtual_boro` varchar(10) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.boro')) VIRTUAL,
  `virtual_zipcode` varchar(5) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.zipcode')) VIRTUAL,
  `virtual_cuisine` varchar(200) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.cuisine_description')) VIRTUAL,
  PRIMARY KEY (`id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`rest_desc_json` is null or json_valid(`rest_desc_json`))
) ENGINE=InnoDB AUTO_INCREMENT=345644 DEFAULT CHARSET=latin1
*/

-- case when virtual_grade_date = '0000-00-00 00:00:00' then NULL else virtual_grade_date end as grade_date,
-- virtual_cuisine_description as cuisine_description,


create or replace view vw_restaurant_inbox as
select
virtual_inspection_date as inspection_date,
case when virtual_grade_date = '0000-00-00 00:00:00' then null else virtual_grade_date end as grade_date,
virtual_cuisine as cuisine,
virtual_boro as boro,
virtual_zipcode as zipcode,
case when virtual_grade = 'null' then null else virtual_grade end as letter_grade,
case virtual_grade when 'A' then 5 when 'B' then 4 when 'C' then 3 when 'D' then 2 when 'F' then 1 else 0 end as grade,
virtual_camis as camis
from restaurant_inbox
;



alter table restaurant_inbox drop column virtual_grade;

alter table restaurant_inbox add virtual_grade varchar(10) as (json_value(rest_desc_json, '$.grade'));



alter table restaurant_inbox drop virtual_grade_date;

alter table restaurant_inbox add virtual_grade_date datetime as (json_value(rest_desc_json, '$.grade_date'));


alter table restaurant_inbox add virtual_camis varchar(20) as (json_value(rest_desc_json, '$.camis'));



create or replace view vw_restaurant_inbox2 as
select
case when virtual_grade_date = '0000-00-00 00:00:00' then null else virtual_grade_date end as grade_date
from restaurant_inbox;


CREATE TABLE `restaurant_inbox` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(400) NOT NULL,
  `rest_desc_json` varchar(5000) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `virtual_inspection_date` datetime GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.inspection_date')) VIRTUAL,
  `virtual_zipcode` varchar(5) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.zipcode')) VIRTUAL,
  `virtual_cuisine` varchar(200) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.cuisine_description')) VIRTUAL,
  `virtual_grade` varchar(200) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.grade')) VIRTUAL,
  `virtual_boro` varchar(20) GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.boro')) VIRTUAL,
  `virtual_grade_date` datetime GENERATED ALWAYS AS (json_value(`rest_desc_json`,'$.grade_date')) VIRTUAL,
  PRIMARY KEY (`id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`rest_desc_json` is null or json_valid(`rest_desc_json`))
) ENGINE=InnoDB AUTO_INCREMENT=346632 DEFAULT CHARSET=latin1;


CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `restuser`@`%` 
    SQL SECURITY DEFINER
VIEW `vw_restaurant_inbox` AS
    SELECT 
        `restaurant_inbox`.`virtual_inspection_date` AS `inspection_date`,
        CASE
            WHEN `restaurant_inbox`.`virtual_grade_date` = '0000-00-00 00:00:00' THEN NULL
            ELSE `restaurant_inbox`.`virtual_grade_date`
        END AS `grade_date`,
        `restaurant_inbox`.`virtual_cuisine` AS `cuisine`,
        `restaurant_inbox`.`virtual_boro` AS `boro`,
        `restaurant_inbox`.`virtual_zipcode` AS `zipcode`,
        `restaurant_inbox`.`virtual_grade` AS `grade`
    FROM
        `restaurant_inbox`
		


alter table restaurant_inbox add virtual_dba varchar(200) as (json_value(rest_desc_json, '$.dba'));		
		

create or replace view vw_restaurant_inbox as
select
virtual_inspection_date as inspection_date,
case when virtual_grade_date = '0000-00-00 00:00:00' then null else virtual_grade_date end as grade_date,
virtual_cuisine as cuisine,
virtual_boro as boro,
virtual_zipcode as zipcode,
case when virtual_grade = 'null' then null else virtual_grade end as letter_grade,
case virtual_grade when 'A' then 5 when 'B' then 4 when 'C' then 3 when 'D' then 2 when 'F' then 1 else 0 end as grade,
virtual_camis as camis,
virtual_dba as dba
from restaurant_inbox
;

