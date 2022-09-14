import os
import shutil
import zipfile

from ..imageProcess.NBIGenerator import getRandom


# rar的解压缩有点麻烦，根据邵老师指示，先不整了
def getCompressedFiles(packageName, user, in_path, out_folder_path):
    folderName = packageName.split('.')[0]
    folderName = "{folderName}_{uid}{rand}".format(folderName=folderName, uid=user, rand=getRandom())
    out_folder_path = out_folder_path + '\\' + folderName
    if os.path.exists(out_folder_path):
        shutil.rmtree(out_folder_path)  # 若输出文件夹以存在，会删除原先的文件夹！！！
    # 解压到指定目录,首先创建一个解压目录
    os.mkdir(out_folder_path)
    with zipfile.ZipFile(file=in_path, mode='r') as zf:
        for old_name in zf.namelist():
            # 获取文件大小，目的是区分文件夹还是文件，如果是空文件应该不好用。
            file_size = zf.getinfo(old_name).file_size
            # 由于源码遇到中文是cp437方式，所以解码成gbk，windows即可正常
            new_name = old_name.encode('cp437').decode('gbk')
            # 拼接文件的保存路径
            new_path = os.path.join(out_folder_path, new_name)
            # 判断文件是文件夹还是文件
            if file_size > 0:
                # 是文件，通过open创建文件，写入数据
                with open(file=new_path, mode='wb') as f:
                    # zf.read 是读取压缩包里的文件内容
                    f.write(zf.read(old_name))
            else:
                # 是文件夹，就创建
                os.mkdir(new_path)
    return folderName


