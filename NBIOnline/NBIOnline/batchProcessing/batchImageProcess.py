
# 指定一个路由，处理这个路径下所有的图片，如果成组则处理并返回True，如果发生错误则返回False
def batchImageProcessing(*args):
    batchID = args[0]
    srcFolderName = args[1]

