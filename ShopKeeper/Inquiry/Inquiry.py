# coding=utf-8
from collections import defaultdict

from Utils import sqlOp
import datetime
import time
import json


def result_map(result_tuple):
    if len(result_tuple) < 2:
        return list(result_tuple)
    res_dic = map(mapper, *result_tuple)
    for i in range(1, len(res_dic)):
        res_dic[i] = len(set(res_dic[i]))
    return res_dic


def split_result_for_month(result_tuple, ts_begin):
    # 4.1 00:00 - 5.1 00:00
    res_dic = defaultdict(list)
    for r in result_tuple:
        ts = int((r[0] - ts_begin) / 86400)
        res_dic[ts + 1].append(r)
    for i in res_dic.keys():
        res_dic[i] = map(mapper, *res_dic[i])
        for j in range(1, len(res_dic[i])):
            res_dic[i][j] = len(set(res_dic[i][j]))
    res_dic['sum'] = result_map(result_tuple)
    return res_dic


def split_result_for_day(result_tuple, ts_begin):
    # 4.1 00:00 - 4.2 00:00
    res_dic = defaultdict(list)
    for r in result_tuple:
        ts = int((r[0] - ts_begin) / 3600)
        res_dic[ts].append(r)
    for i in res_dic.keys():
        res_dic[i] = map(mapper, *res_dic[i])
        for j in range(1, len(res_dic[i])):
            res_dic[i][j] = len(set(res_dic[i][j]))
    res_dic['sum'] = result_map(result_tuple)
    return res_dic


def mapper(*result):
    if type(result[0]) == long:
        return 0
    else:
        res = []
        for i in result:
            if len(i) != 0:
                res += i.split(" ")
        return res


def print_result(result):
    if len(result) < 2:
        print "No data"
        return
    print "客流量: ", len(set(result[1]))
    print "入店量: ", len(set(result[2]))
    print "入店率: %2s%%" % (100 * len(set(result[2])) / len(set(result[1])))
    print "跳出率: %2s%%" % (100 * len(set(result[3])) / len(set(result[1])))
    print "深访率: %2s%%" % (100 * len(set(result[4])) / len(set(result[1])))
    # print "跳出量: ", len(set(result[3]))
    # print "深访量: ", len(set(result[4]))
    print "新顾客: ", len(set(result[5]))
    print "老顾客: ", len(set(result[6]))


def get_results_for_day(year, month, day):
    date_begin = datetime.date(year, month, day)
    ts_begin = time.mktime(date_begin.timetuple())
    ts_end = ts_begin + 86400
    result_tuple = sqlOp.inquiry(ts_begin, ts_end)

    return json.dumps(split_result_for_day(result_tuple, ts_begin))


def get_results_for_month(year, month):
    date_begin = datetime.date(year, month, 1)
    if month == 12:
        date_end = datetime.date(year + 1, 1, 1)
    else:
        date_end = datetime.date(year, month + 1, 1)

    ts_begin = time.mktime(date_begin.timetuple())
    ts_end = time.mktime(date_end.timetuple())

    result_tuple = sqlOp.inquiry(ts_begin, ts_end)

    return json.dumps(split_result_for_month(result_tuple, ts_begin))


def get_result_for_mac_all():
    result_list = sqlOp.scan()
    return result_list


def get_result_for_mac(mac):
    result_list = sqlOp.get(mac)
    return result_list
