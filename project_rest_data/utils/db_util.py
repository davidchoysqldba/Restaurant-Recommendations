import pymysql as mariadb

class dbUtil:
    def __init__(self, host, user, passwd, db, is_commit=False):
        #host='192.168.1.129',
        #user='lemp',
        #passwd='123454',
        #db='restaurant_db'
        self.conn = mariadb.connect(
            host = host,
            user = user,
            passwd = passwd,
            db = db,
            use_unicode=True,
            charset="utf8",
            autocommit=is_commit
        )

    def executeQuery(self, sql_statement):
        resultset = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_statement)
            data = cursor.fetchall()
            resultset = data
            cursor.close()

        except Exception as e:
            print('Connection Failed!\nError Code is %s;\nError Content is %s;' % (e.args[0],e.args[1]))

        return resultset


    def executeManyQuery(self, sql_statement, param_list):
        resultset = None
        try:
            cursor = self.conn.cursor()
            cursor.executemany(sql_statement, param_list)
            data = cursor.fetchall()
            resultset = data
            cursor.close()

        except Exception as e:
            print('Connection Failed!\nError Code is %s;\nError Content is %s;' % (e))

        return resultset


    def executeCommit(self):
        try:
            self.conn.commit()
        except Exception as e:
            print('Failed to Commit!\nError Code is %s;\nError Content is %s;' % (e.args[0],e.args[1]))


def main():
    dbobj = dbUtil("192.168.1.221", "restuser", "restuser", "restaurantdb", True)
    #print(dbobj)
    if dbobj:
        json_string = '{"action":"Violations were cited in the following area(s).","boro":"MANHATTAN","building":"42","camis":41623086,"critical_flag":"Critical","cuisine_description":"Chinese","dba":"SING KEE SEAFOOD RESTAURANT","grade":null,"grade_date":null,"inspection_date":"2015-04-23T00:00:00.000","inspection_type":"Cycle Inspection \/ Initial Inspection","phone":2122338666,"record_date":"2018-01-03T06:00:54.000","score":23.0,"street":"BOWERY","violation_code":"04M","violation_description":"Live roaches present in facility''s food and\/or non-food areas.","zipcode":10013}'
        #resultset = dbobj.executeQuery("select 1 as user_id, 'John' as user_name union select 2 as user_id, 'Danny' as user_name;")
        #qry_string = "insert into restaurant_inbox (file_name, rest_desc_json) values ('1.json', '" + json_string + "');"
        #print(qry_string)
        #dbobj.executeQuery(qry_string)


        qry_string = "insert into restaurant_inbox (file_name, rest_desc_json) values (%s, %s)"
        json_list = [
            #('restaurant_data_2017_11_21.json', json_string)
            ('restaurant_data_2017_12_05.json', json_string)
            #('1.json', json_string),
            #('2.json', json_string)
        ]
        #dbobj.executeManyQuery(qry_string, json_list)

        resultset = dbobj.executeQuery("select * from restaurant_inbox;")
        for r in resultset:
            print(r)
        #print(type(resultset))

if __name__ == "__main__":
    main()

