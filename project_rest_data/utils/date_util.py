import dateutil
import datetime

def getValidDateList(file_pattern, date_list, valid_datelist):
    #print(valid_datelist)
    #print(date_list)
    return_list = sorted(list(filter(lambda l: (l[-15:-5] not in valid_datelist), date_list)))
    return return_list


def getDateRange(date):
    from datetime import date as d, timedelta
    import dateutil.relativedelta
    N = 3
    date_end = d.today() - timedelta(days=N)
    N = 1
    date_begin = date_end + dateutil.relativedelta.relativedelta(months=-1*N)
    print("day range between: ", date_begin, date_end)
    return date_begin, date_end


def getDateList(date):
    from datetime import timedelta
    date_list = []
    #print("day range between: ", date_begindatetime.date.today()
    date_begin, date_end = getDateRange(date)
    date_loop = date_begin
    while date_loop <= date_end:
        date_list.append(date_loop)
        date_loop = date_loop + timedelta(days=1)  # replace the interval at will
    return date_list


def getDateListString(date):
    return_list = []
    mylist = getDateList(date)
    for i in mylist:
        return_list.append(i.strftime('%Y_%m_%d'))
    return return_list


def main():
    date_list = getDateList(datetime.date.today())
    for l in date_list:
        pass


if __name__ == "__main__":
    main()
