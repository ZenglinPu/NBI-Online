# 用户等级权限管理相关操作
import time

from ..dataManagement.db_connection import getConnection, getTable, NBITABLE


def getUserRankByUID(uid):
    conn = getConnection()
    table_UserInfo = getTable(conn, NBITABLE.UserInfo)
    if table_UserInfo.find_one({"UID": uid})['expiresTime'] > time.time():
        conn.close()
        return 2
    conn.close()
    return 1


def checkUploadTime(uid):
    conn = getConnection()
    table_UserInfo = getTable(conn, NBITABLE.UserInfo)
    # print(table_PhotoInfo.find_one({"UID": uid})['TIMES_generate'])
    if table_UserInfo.find_one({"UID": uid})['TIMES_generate'] <= 0:
        conn.close()
        return False
    conn.close()
    return True
