# 每24小时去除数据库中已经过期的图片数据及其磁盘中的图片本身
import time

from apscheduler.schedulers.background import BackgroundScheduler
from ..dataManagement.dbFunction import deleteAllExpiredImages


# TODO: 担心删除有用数据，故尚未实际启动
class GCTask:
    def __init__(self, gc=False):
        super().__init__()
        self.gc = gc
        self.job = None
        self.scheduler = BackgroundScheduler(timezone='Asia/Shanghai')

    def GCImageData(self):
        # 删除过期图片及数据库中信息
        deleteAllExpiredImages()

    def nothing(self):
        pass

    def start(self, hours=24):
        if self.gc == True:
            self.job = self.scheduler.add_job(self.GCImageData, trigger='interval', hours=hours, id='gc')
            print("Start image GC")
        else:
            self.job = self.scheduler.add_job(self.nothing, trigger='interval', hours=hours, id='gc')
            print("Without image GC")
        self.scheduler.start()

    def delete(self):
        self.scheduler.remove_job(self.job)
        self.job = None

    def shutdown(self):
        self.scheduler.shutdown()

