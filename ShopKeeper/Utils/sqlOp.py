# coding=utf-8
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *
from Config import Config
import MySQLdb
import traceback

hbase_host = Config.MyConfigParser.get("hbase", "hbase_host")
hbase_port = Config.MyConfigParser.get("hbase", "hbase_port")

transport = TSocket.TSocket(hbase_host, hbase_port)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = Hbase.Client(protocol)

mysql_host = Config.MyConfigParser.get("mysql", "mysql_host")
mysql_user = Config.MyConfigParser.get("mysql", "mysql_user")
mysql_pw = Config.MyConfigParser.get("mysql", "mysql_pw")
mysql_database = Config.MyConfigParser.get("mysql", "mysql_database")


def storage(row_key, cols, tableName='Customers'):
    mutations = []
    for k, v in cols.items():
        col = Mutation(column=str(k), value=str(v))
        mutations.append(col)
    transport.open()
    client.mutateRow(tableName, row_key, mutations, None)
    transport.close()


def get(row_key, tableName='Customers'):
    transport.open()
    row = client.getRow(tableName, row_key, None)
    transport.close()
    return row


def scan(tableName='Customers'):
    transport.open()
    scan = TScan()
    id = client.scannerOpenWithScan(tableName, scan, None)
    result = client.scannerGetList(id, 4*100)
    transport.close()
    return result


def get_ver(mac, col, ver=100, tableName='Customers'):
    transport.open()
    row = client.getVer(tableName, mac, col, ver, None)
    transport.close()
    return row


def save_results(timestamp, Result):
    db = MySQLdb.connect(mysql_host, mysql_user, mysql_pw, mysql_database)
    cursor = db.cursor()
    tup = (timestamp,) + tuple([" ".join(i) for i in Result])


    sql = """INSERT INTO Results(
    		t_time,t_flow, t_inner, t_outer, t_deepin, t_new, t_old)
    		VALUES (%s, "%s", "%s", "%s", "%s", "%s", "%s");""" % tup

    sql = sql.replace("'","\'")
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        traceback.print_exc()
    db.close()


def inquiry(ts_begin, ts_end):
    db = MySQLdb.connect(mysql_host, mysql_user, mysql_pw, mysql_database)
    cursor = db.cursor()

    sql = '''SELECT t_time, t_flow, t_inner, t_outer, t_deepin, t_new, t_old
    FROM Results WHERE t_time >= %s and t_time <= %s;''' % (ts_begin, ts_end)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        traceback.print_exc()
    db.close()
    return cursor.fetchall()


def create_hbase_table(tableName='Customers'):
    transport.open()
    contents = ColumnDescriptor(name='VisitingInfo:', maxVersions=1000)
    client.createTable(tableName, [contents])
    transport.close()
