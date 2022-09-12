import pymongo
from ..dataManagement.db_connection import getConnection, getTable, NBITABLE


# '''
# 图片附加信息表：PhotoAdditionInfo
# | 字段名          | 类型     | 含义                 |
# | -------------- | ------- | -------------------------------------------------------------------------|
# | GID            | String  | 图片的_id                                                                 |
# | sampleName     | String  | 标本名                                                                    |
# | part           | String  | 标本部位名                                                                |
# | preDiagnosis   | String  | 预诊断结论，可多选，|分割                                                  |
# | remark         | String  | 标本备注信息，随意输入                                                     |
# | pathologic     | String  | 病理诊断结论，可多选，|分割                                                |
# | differentiation| Integer | 分化程度多选：‘0’：不适用 ‘1‘：低分化 ‘2’：中分化 ‘3‘：高分化 多选，|分割    |
# | infiltration   | Integer | 浸润深度：单选 0：粘膜上皮层，1:粘膜固有层，2:粘膜肌层3:粘膜下层（文本录入，单位μm），4:固有肌层|
# | cuttingEdge    | Boolean | 水平切缘 1-阳性；2-阴性                                                    |
# '''

class imageAdditionInfo:
    def __init__(self, gid, sampleName=None, part=None, preDiagnosis=None, remark=None, pathologic=None,
                 differentiation=None, infiltration=None, cuttingEdge=None):
        self.gid = gid
        self.sampleName = sampleName
        self.part = part
        self.preDiagnosis = preDiagnosis
        self.remark = remark
        self.pathologic = pathologic
        self.differentiation = differentiation
        self.infiltration = infiltration
        self.cuttingEdge = cuttingEdge

    def getDict(self):
        ret = dict()
        ret['gid'] = self.gid
        ret['sampleName'] = self.sampleName
        ret['part'] = self.part
        ret['preDiagnosis'] = self.preDiagnosis
        ret['remark'] = self.remark
        ret['pathologic'] = self.pathologic
        ret['differentiation'] = self.differentiation
        ret['infiltration'] = self.infiltration
        ret['cuttingEdge'] = self.cuttingEdge
        return ret

    def saveNewAdditionalInfo(self):
        conn = getConnection()
        table = getTable(conn, NBITABLE.PhotoAdditionInfo)
        # print(self.getDict())
        ret = table.insert_one(self.getDict())
        # conn.close()
        return ret

    def replaceData(self):
        print("Update Data at GID={u}".format(u=self.gid))
        conn = getConnection()
        table = getTable(conn, NBITABLE.PhotoAdditionInfo)
        condition = {'GID': self.gid}
        result = table.replace_one(condition, self.getDict())  # 执行数据库更新操作
        # conn.close()
        return result
