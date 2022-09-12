import pymongo

global_connection = None
# DB连接的封装, 长连接

def get_connection():
    global global_connection
    while global_connection is None:
        try:
            if global_connection is not None:
                global_connection.close()
            global_connection = pymongo.MongoClient(
                'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
        except Exception as e:
            global_connection = None

    return global_connection
