# coding=utf-8
import datetime
import time
from Config import Config

format = Config.MyConfigParser.get("json_loads", "time_format")


def str_to_datetime(time_str):
    return datetime.datetime.strptime(time_str, format)


def str_to_timestamp(time_str):
    d = datetime.datetime.strptime(time_str, format)
    return int(time.mktime(d.timetuple()))


def second_to_time(value):
    value = float(value)
    hour = int(value / 3600)
    min = int((value % 3600) / 60)
    sec = int(value % 60)
    return str(hour) + "小时" + str(min) + "分钟" + str(sec) + "秒"


def liveness_tran(value):
    if value == "High":
        return "高"
    elif value == "Medium":
        return "中"
    else:
        return "低"
