import sys
import os
import unittest

env_list = ['DEV', 'CI', 'STAGING', 'PROD']

sys.path.insert(0, os.getcwd())

from config import config
#print(config.cfg['ENV'])
#print(config.db_config)
from utils.db_util import dbUtil#

class TestDB(unittest.TestCase):
    """
    Test the DB Unittest function
    """

    def test_db_config(self):
        """
            Test database config settings
        """
        env_var = config.cfg['ENV']
        if env_var in env_list:
            result = True
        else:
            result = False
        self.assertEqual(result, True)

    def test_conn(self):
        """
            Test database connection success
        """

        dbconn = dbUtil(config.db_config['host'], config.db_config['username'], config.db_config['password'],
                        config.db_config['database_name'])
        resultset = dbconn.executeQuery("select 1 col1")
        if len(resultset) > 0:
            result = True
        else:
            result = False
        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()