
import datetime

week_day_dict = {
    0 : '星期一',
    1 : '星期二',
    2 : '星期三',
    3 : '星期四',
    4 : '星期五',
    5 : '星期六',
    6 : '星期天',
}

part_day = ["2020-01-24","2020-01-27","2020-01-28","2020-01-29","2020-01-30","2020-01-31","2020-01-01",
            "2019-12-25","2019-12-26","2020-04-06","2020-05-01","2020-04-06","2020-04-10","2020-06-25","2020-06-26"]

# must YY-MM-DD
def IsTurnOn(dt):
    date = datetime.datetime.strptime(dt, '%Y-%m-%d').date()
    if dt in part_day:
        return False
    day = date.weekday()
    if day in [0,1,2,3,4]:
        return True
    else:
        return False


# last 60 day dt
def getLast60TurnOnDtList(dt):
    dates = []
    date = datetime.datetime.strptime(dt, "%Y-%m-%d")
    res_dt = dt[:]
    for i in range(60):
        if IsTurnOn(res_dt):
            dates.append(res_dt)
        date = date + datetime.timedelta(-1)
        res_dt = date.strftime("%Y-%m-%d")
    return dates


def getDtList(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates



if __name__ == '__main__':
    print(getLast60TurnOnDtList("2020-02-03"))