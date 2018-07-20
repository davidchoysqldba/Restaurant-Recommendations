import datetime

import luigi
import pandas as pd

from utils import date_util
from config import config

# import luigi.contrib.hadoop
# import luigi.contrib.hdfs
# import luigi.contrib.postgres

#download_url = config.download_url
#download_root_folder = config.download_root_folder
#download_restaurant_file_pattern =

class DownloadRestaurantData(luigi.Task):
    #set default date if no DateParameter
    date = luigi.DateParameter(default=datetime.date.today())

    def run(self):
        date_part = self.date.strftime('%Y-%m-%d') + "T00:00:00.000"
        url = config.download_url + date_part
        #print("downloading url: " + url)
        with self.output().open('w') as f:
            f.write(pd.read_json(url).to_json(orient='records', lines=True))

    def output(self):
        return luigi.LocalTarget(self.date.strftime(config.download_root_folder + '/data/' + config.download_restaurant_file_pattern + '_%Y_%m_%d.json'))


class DownloadRestaurantDataForDates(luigi.Task):
    #set default date if no DateParameter
    date = luigi.DateParameter(default=datetime.date.today())

    def requires(self):
        date_list = date_util.getDateList(self.date)
        #print([date_loop for date_loop in date_list])
        return [DownloadRestaurantData(date_loop) for date_loop in date_list]

    def run(self):
        with self.output().open('w') as output:
            output.write("Done")

    def output(self):
        #print("filename: ", self.date.strftime('data/restaurant_data_range_%Y_%m_%d.json'))
        return luigi.LocalTarget(self.date.strftime(config.download_root_folder + '/log/' + config.download_restaurant_log_pattern + '_%Y_%m_%d.log'))
