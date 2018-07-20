from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import Row, functions as F
from datetime import datetime
from pyspark.sql.window import Window

#from pyspark import SparkContext
from luigi.contrib.spark import PySparkTask, SparkSubmitTask

import luigi

#from utils import date_util
from utils.db_util import dbUtil

#from utils import date_util

startTime = datetime.now()

#conf = SparkConf().setMaster("local").setAppName("SaveRecommendation")
#sc = SparkContext(conf = conf)
#sqlContext = SQLContext(sc)

class SaveRecommendationZipCode(PySparkTask):

    dt = luigi.DateParameter(default=datetime.today())

    def main(self, sc, *args):
        sqlContext = SQLContext(sc)
        #Connect to MySQL table and return data frame
        #df_rest_data = sqlContext.read.format("jdbc").options(url="jdbc:mysql://192.168.1.221:3306/restaurantdb",driver="com.mysql.jdbc.Driver",dbtable="vw_restaurant_inbox",user="restuser",password="restuser").load()
        df_rest_data = sqlContext.read.format("jdbc").options(url="jdbc:mysql://192.168.1.221:3306/restaurantdb",
                                                              driver="com.mysql.jdbc.Driver",
                                                              dbtable="vw_restaurant_inbox", user="restuser",
                                                              password="restuser").load()

        #aggragate data and return dataframe
        df_rest_data2 = df_rest_data.filter("zipcode is not null").groupBy("zipcode", "boro", "camis", "dba").agg(F.avg("grade").alias("grade_avg"), F.count("*").alias("grade_count"))

        df_rest_data3 = df_rest_data2.select("zipcode", "dba", "boro", "grade_avg", "grade_count", F.row_number().over(Window.partitionBy("zipcode").orderBy(F.desc("grade_avg"), F.desc("grade_count"))).alias("row_num")).filter("row_num = 1")

        import time
        insert_list = []
        for r in df_rest_data3.collect():
            #insert_list.append(r(i) for i in (range(0, len(r))))
            insert_list.append((r.zipcode, r.dba, r.boro, r.grade_avg, r.grade_count, time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))

        # for r in insert_list:
        #     print(r)
        # insert_list = []
        # for r in df_rest_data3.collect():
        #     mydict = r.asDict(True)
        #     mydict['date_created'] = datetime.now()
        #     mydict['date_modifed'] = datetime.now()
        #     insert_list.append(mydict)

        #for r in insert_list:
        #    print(r)

        dbobj = dbUtil("192.168.1.221", "restuser", "restuser", "restaurantdb")
        if dbobj:
            #dbobj.executeQuery('truncate table recommendation_zipcode;')
            dbobj.executeQuery('update recommendation_zipcode set is_latest = 0;')
            dbobj.executeManyQuery("insert into recommendation_zipcode (zipcode, dba, boro, grade_average, grade_count, date_created, date_modified) values (%s, %s, %s, %s, %s, %s, %s)", insert_list)
            dbobj.executeQuery('update recommendation_zipcode set is_latest = 1 where is_latest is NULL;')
            dbobj.executeCommit()

            with self.output().open('w') as output:
                output.write("Done")

        print(datetime.now() - startTime)

    def output(self):
        return luigi.LocalTarget(self.dt.strftime('data/save_recommend_zipcode_%Y_%m_%d.log'))


class SaveRecommendationBoro(PySparkTask):

    dt = luigi.DateParameter(default=datetime.today())

    def main(self, sc, *args):
        sqlContext = SQLContext(sc)
        # Connect to MySQL table and return data frame
        df_rest_data = sqlContext.read.format("jdbc").options(url="jdbc:mysql://192.168.1.221:3306/restaurantdb",
                                                              driver="com.mysql.jdbc.Driver",
                                                              dbtable="vw_restaurant_inbox", user="restuser",
                                                              password="restuser").load()

        # aggragate data and return dataframe
        df_rest_data2 = df_rest_data.filter("boro is not null").groupBy("boro", "dba").agg(F.avg("grade").alias("grade_avg"), F.count("*").alias("grade_count"))
        df_rest_data3 = df_rest_data2.select("boro", "dba", "grade_avg", "grade_count", F.row_number().over(Window.partitionBy("boro").orderBy(F.desc("grade_avg"), F.desc("grade_count"))).alias("row_num")).filter("row_num = 1")


        import time
        insert_list = []
        for r in df_rest_data3.collect():
            # insert_list.append(r(i) for i in (range(0, len(r))))
            insert_list.append((r.boro, r.dba, r.grade_avg, r.grade_count,
                                time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))

        # for r in insert_list:
        #     print(r)
        # insert_list = []
        # for r in df_rest_data3.collect():
        #     mydict = r.asDict(True)
        #     mydict['date_created'] = datetime.now()
        #     mydict['date_modifed'] = datetime.now()
        #     insert_list.append(mydict)

        dbobj = dbUtil("192.168.1.221", "restuser", "restuser", "restaurantdb")
        if dbobj:
            #dbobj.executeQuery('truncate table recommendation_boro;')
            dbobj.executeQuery('update recommendation_boro set is_latest = 0;')
            dbobj.executeManyQuery("insert into recommendation_boro (boro, dba, grade_average, grade_count, date_created, date_modified) values (%s, %s, %s, %s, %s, %s)",insert_list)
            dbobj.executeQuery('update recommendation_boro set is_latest = 1 where is_latest is NULL;')
            dbobj.executeCommit()

            with self.output().open('w') as output:
                output.write("Done")

        print(datetime.now() - startTime)

    def output(self):
        return luigi.LocalTarget(self.dt.strftime('data/save_recommend_boro_%Y_%m_%d.log'))
