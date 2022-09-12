# 每24小时去除数据库中已经过期的图片数据及其磁盘中的图片本身
import time

from apscheduler.schedulers.background import BackgroundScheduler
from ..dataManagement.dbFunction import deleteAllExpiredImages


# TODO: 担心删除有用数据，故尚未实际启动
class GCTask:
    def __init__(self):
        super().__init__()
        self.job = None
        self.scheduler = BackgroundScheduler(timezone='Asia/Shanghai')

    def GCImageData(self):
        # 删除过期图片及数据库中信息
        deleteAllExpiredImages()

    def start(self, hours=24):
        self.job = self.scheduler.add_job(self.GCImageData, trigger='interval', hours=hours, id='gc')
        self.scheduler.start()

    def delete(self):
        self.scheduler.remove_job(self.job)
        self.job = None

    def shutdown(self):
        self.scheduler.shutdown()


gcTask = GCTask()
gcTask.start(hours=2)

print(1000)

time.sleep(50)

gcTask.shutdown()
