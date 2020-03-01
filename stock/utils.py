
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

# must YY-MM-DD
def IsTurnOn(dt):
    date = datetime.datetime.strptime(dt, '%Y-%m-%d').date()
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
    print(getLast30TurnOnDtList("2020-02-28"))