# coding=utf-8
import datetime
import json
from collections import defaultdict
import sys
import os


def cmp(a, b):
    if a['time'] > b['time']:
        return 1
    elif a['time'] < b['time']:
        return -1
    else:
        return 0


reload(sys)
sys.setdefaultencoding('utf8')
f = file("spark_data_3.json", "r")
input = []

for i in f.readlines():
    input.append(json.loads(i))

f.close()
res = defaultdict(list)
format = '%a %b %d %H:%M:%S %Y'

for i in input:
    time = datetime.datetime.fromtimestamp(int(i['time']))
    time_str = datetime.datetime.strftime(time, format)
    str = '''{"mac":"%s","rssi":"%s","range":"%s"}''' % (i['mac'], i['rssi'], i['range'])
    res[time_str].append(str)

res = [{'time': k, 'items': v} for k, v in res.items()]

for i in res:
    time_str = i['time']
    time = time_str.split(" ")
    path = "./json/"

    if not os.path.exists(path):
        os.makedirs(path)

    path = path + time[3].replace(":", "_") + ".txt"
    str = ','.join(i['items'])
    json_str = '''{"id":"00166048","mmac":"a2:20:a6:16:60:48","rate":"1","wssid":"rockme","wmac":"ea:80:2e:aa:bb:5d","time":"%s","lat":"36.000011","lon":"120.122498","addr":"山东省青岛市黄岛区辛安街道碧波路;步云路与碧波路路口东74","data":[%s]}''' % (
    i['time'], str)

    f = open(path, "w")
    f.write(json_str)
    f.close()
