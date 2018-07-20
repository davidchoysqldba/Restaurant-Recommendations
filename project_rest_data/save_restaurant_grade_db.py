import datetime
import glob
import os

import luigi

from utils import date_util
from utils.db_util import dbUtil
from config import config

class FindRestaurantData(luigi.Task):

    dt = luigi.DateParameter(default=datetime.date.today())

    def requires(self):
        #list within 1 month
        #------------------------------------------------------
        valid_datelist = date_util.getDateListString(self.dt)

        file_folder = config.download_root_folder + '/data/'
        #file_folder = './data/'
        file_folder = os.path.abspath(file_folder)
        #print('abs folder path: ', file_folder)

        file_pattern = 'restaurant_data_*.json'
        #print(file_folder + file_pattern)

        #Search all *.json files downloaded/saved
        # ------------------------------------------------------
        saved_list = glob.glob(file_folder + '/' + file_pattern)

        #print(saved_list)
        #valid date list are files downloaded within 30 days
        validated_datelist = sorted(list(filter(lambda l: (l[-15:-5] in valid_datelist), saved_list)))
        # print(validated_datelist)

        #dbobj = dbUtil("192.168.1.221", "restuser", "restuser", "restaurantdb", True)
        dbobj = dbUtil(config.db_config['host'], config.db_config['username'], config.db_config['password'],
                        config.db_config['database_name'])

        if dbobj:
            resultobj = dbobj.executeQuery("select distinct file_name from restaurant_inbox order by file_name desc")
            #print(resultobj)

        #processed list is the list inserted into database
        processed_filelist = [' '.join(item) for item in resultobj]
        # print("--------------------\n")
        # print(processed_filelist)

        #dbinsert list is the new file list hasn't inserted into database
        dbinsert_datelist = sorted(list(filter(lambda l: (l[-31:] not in processed_filelist), validated_datelist)))
        # print("--------------------\n")
        # print(dbinsert_datelist)
        #for r in dbinsert_datelist:
        #    print(r)

        return [SaveRestaurantData(filename) for filename in dbinsert_datelist]
        #rest_businessobj.saveValidatedJsonFile(validated_datelist)

    def run(self):
        with self.output().open('w') as output:
            output.write("Done")

    def output(self):
        #print(self.dt.strftime(config.download_root_folder + '/log/' + config.find_restaurant_file_pattern + '_%Y_%m_%d.log'))
        return luigi.LocalTarget(self.dt.strftime(config.download_root_folder + '/log/' + config.find_restaurant_file_pattern + '_%Y_%m_%d.log'))


class SaveRestaurantData(luigi.Task):
    filename = luigi.Parameter()
    dt = datetime.date.today()

    def run(self):
        #pass

        jsonfilename = self.filename[-31:]
        #print("jsonfilename: ", jsonfilename)

        insert_list = []
        file = open(self.filename, 'r')
        json_content = file.readlines()
        if len(json_content) == 0:
            insert_list.append((jsonfilename, None))
        else:
            for line in json_content:
                insert_list.append((jsonfilename, line))
            file.close()

        qry_string = "insert into restaurant_inbox (file_name, rest_desc_json) values (%s, %s)"
        #dbobj = dbUtil("192.168.1.221", "restuser", "restuser", "restaurantdb", True)
        dbobj = dbUtil(config.db_config['host'], config.db_config['username'], config.db_config['password'],
                        config.db_config['database_name'])
        try:
            if dbobj:
                dbobj.executeQuery("delete from restaurant_inbox where file_name = '" + jsonfilename + "'")
                dbobj.executeManyQuery(qry_string, insert_list)
            #print('filename: ', self.filename)
            #dt = datetime.date.today()
            #valid_datelist = date_util.getDateListString(self.dt)

            #rest_businessobj.saveValidatedJsonFile(validated_datelist)

            with self.output().open('w') as output:
                output.write("Done")
        except Exception as e:
            print('Failed Insert ', self.filename, ': ', e)

    def output(self):
        print(self.dt.strftime(config.download_root_folder + '/log/' + config.save_restaurant_log_pattern + '_' + self.filename[-31:] + '_%Y_%m_%d.log'))
        return luigi.LocalTarget(self.dt.strftime(config.download_root_folder + '/log/' + config.save_restaurant_log_pattern + '_' + self.filename[-31:] + '_%Y_%m_%d.log'))
