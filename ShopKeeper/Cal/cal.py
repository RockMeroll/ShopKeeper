# coding=utf-8
import sys
import thread

from Config import Config
from Utils import sqlOp, utils


# Constant
# metre
FLOW_RANGE = Config.MyConfigParser.getint("user_config", "FLOW_RANGE")
SHOP_RANGE = Config.MyConfigParser.getint("user_config", "SHOP_RANGE")
# second
SCAN_CYCLE = Config.MyConfigParser.getint("user_config", "SCAN_CYCLE")
DEEP_IN_TIME = Config.MyConfigParser.getint("user_config", "DEEP_IN_TIME")
QUICK_EXIT_TIME = Config.MyConfigParser.getint("user_config", "QUICK_EXIT_TIME")

HIGH_LIVENESS = Config.MyConfigParser.getint("user_config", "HIGH_LIVENESS")
MEDIUM_LIVENESS = Config.MyConfigParser.getint("user_config", "MEDIUM_LIVENESS")


def get_data(sqlContext, file_path):
    dataframe = sqlContext.read.json(file_path)
    return dataframe.collect()[0].asDict()


# 是否客流量
def is_flow(mac, range_):
    if range_ < FLOW_RANGE:
        return [mac]
    else:
        return []


# 入店量
def is_inner(mac, range_):
    if range_ < SHOP_RANGE:
        return [mac]
    else:
        return []


# 是否跳出
def is_outer(mac, range_, stay_in_time):
    if range_ > SHOP_RANGE and stay_in_time < QUICK_EXIT_TIME:
        return [mac]
    else:
        return []


# 是否深访

def is_deep_in(mac, range_, stay_in_time):
    if range_ < SHOP_RANGE and stay_in_time > DEEP_IN_TIME:
        return [mac]
    else:
        return []


# 新顾客
def is_new(mac, range_, history_info):
    if len(history_info) == 0 and range_ < SHOP_RANGE:
        return [mac]
    return []


# 老顾客
def is_old(mac, range_, stay_in_time, history_info):
    if len(history_info) != 0 and range_ < SHOP_RANGE and stay_in_time == 0:
        return [mac]
    return []


# 活跃度
def liveness(visit_cycle):
    if visit_cycle <= HIGH_LIVENESS:
        return "High"
    elif visit_cycle <= MEDIUM_LIVENESS:
        return "Medium"
    else:
        return "Low"


# 驻店时长
def get_stay_in_time(range_, history_info, now):
    if len(history_info) == 0 or range_ > SHOP_RANGE:
        return 0
    else:
        now = utils.str_to_datetime(now)
        first = utils.str_to_datetime(history_info[0].value)
        second = utils.str_to_datetime(history_info[-1].value)
        if (now - first).total_seconds() > SCAN_CYCLE:
            return 0
        elif (first - second).total_seconds() <= SCAN_CYCLE * len(history_info) - 1:
            return (now - second).total_seconds()
        else:
            i = 0
            for i in range(0, len(history_info) - 1):
                first = utils.str_to_datetime(history_info[i].value)
                second = utils.str_to_datetime(history_info[i + 1].value)
                time_delta = first - second
                if time_delta.total_seconds() > SCAN_CYCLE:
                    break
            time_last = utils.str_to_datetime(history_info[i].value)
            return (now - time_last).total_seconds()


# 来访周期
def get_visit_cycle(history_info, time):
    if len(history_info) == 0:
        return 0
    now = utils.str_to_datetime(time)
    first = utils.str_to_datetime(history_info[0].value)
    if (now - first).total_seconds() > SCAN_CYCLE:
        return (now - first).total_seconds()
    i = 0
    for i in range(1, len(history_info)):
        first = utils.str_to_datetime(history_info[i - 1].value)
        second = utils.str_to_datetime(history_info[i].value)
        time_delta = first - second
        if time_delta.total_seconds() > SCAN_CYCLE:
            break
    if i + 1 == len(history_info):
        return 0

    first = utils.str_to_datetime(history_info[i].value)
    return (now - first).total_seconds()


def mapper(data, time):
    mac = data['mac']
    range_ = float(data['range'])
    visit_cycle = 0
    stay_in_time = 0
    history_info = sqlOp.get_ver(mac, "VisitingInfo:LastVisit")

    if len(history_info) != 0:
        visit_cycle = get_visit_cycle(history_info, time)
        stay_in_time = get_stay_in_time(range_, history_info, time)

    if is_inner(mac, range_):
        dic = {"VisitingInfo:LastVisit": time,
               "VisitingInfo:VisitCycle": visit_cycle,
               "VisitingInfo:StayInTime": stay_in_time,
               "VisitingInfo:Liveness": liveness(visit_cycle)
               }
        sqlOp.storage(mac, dic)

    return [mac], \
           is_flow(mac, range_), \
           is_inner(mac, range_), \
           is_outer(mac, range_, stay_in_time), \
           is_deep_in(mac, range_, stay_in_time), \
           is_new(mac, range_, history_info), \
           is_old(mac, range_, stay_in_time, history_info), \
           [stay_in_time], \
           [liveness(visit_cycle)], \
           [visit_cycle]


def reducer(a, b):
    mac = a[0] + b[0]
    is_flow_ = a[1] + b[1]
    is_inner_ = a[2] + b[2]
    is_outer_ = a[3] + b[3]
    is_stay_in_ = a[4] + b[4]
    is_new_ = a[5] + b[5]
    is_old_ = a[6] + b[6]
    stay_in_time_ = a[7] + b[7]
    liveness_ = a[8] + b[8]
    visit_cycle_ = a[9] + b[9]
    return mac, is_flow_, is_inner_, is_outer_, is_stay_in_, is_new_, is_old_, \
           stay_in_time_, liveness_, visit_cycle_


def cal(file_path, sc, sqlContext):
    data_dic = get_data(sqlContext, file_path)
    time_str = data_dic['time']
    pass_flow_data = data_dic['data']
    pass_flow_data_rdd = sc.parallelize(pass_flow_data)
    result = pass_flow_data_rdd.map(lambda x: mapper(x, time_str))\
        .reduce(reducer)

    ts = utils.str_to_timestamp(time_str)
    # save result to mysql
    thread.start_new_thread(sqlOp.save_results, (ts, result[1:7]))
    print file_path, "Done"
    # print "客流量: ", result[1]
    # print "入店量: ", result[2]
    # print "跳出量: ", result[3]
    # print "深访量: ", result[4]
    # print "新顾客: ", result[5]
    # print "老顾客: ", result[6]
    #
    # print "驻店时长：", result[7]
    # print "活跃度: ", result[8]
    # print "来访周期：", result[9]


