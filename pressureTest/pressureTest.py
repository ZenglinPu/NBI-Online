import json
import threading
import time

import matplotlib.pyplot as plt
import requests
from requests import Request, Session

TEST_USER_NUM = 3
TEST_PROCEDURE = {
    "isLogin": True,
    "isUpload": True,
    "isGenerate": True,
}
WAIT_TIME_MAX = {
    "isLogin": 5,
    "isUpload": 400,
    "isGenerate": 45,
}

loginCheckAccountData = []
for i in range(min(TEST_USER_NUM, 100)):
    loginCheckAccountData.append(dict(
        {
            "uid": str(i + 1) * 3 + "@" + str(i + 1) * 3 + ".com",
            "pwd": "123",
            "token": "",
        }
    ))

if TEST_PROCEDURE['isLogin']:
    loginCheckData = [json.dumps(x) for x in loginCheckAccountData]
    loginConsumeTimeList = []
    loginUrl = "http://49.232.229.126:7000/NBI/User/checkLogin/"


    def sendLoginRequest(*args):
        startTime = time.time()
        res = requests.post(url=loginUrl,
                            headers={"Content-Type": "application/json"},
                            data=args[0])
        print(res.json())
        args[1]['token'] = res.json()['token']
        consumeTime = time.time() - startTime
        loginConsumeTimeList.append(consumeTime)


    # login
    for threadID in range(len(loginCheckAccountData)):
        preProcessThread = threading.Thread(target=sendLoginRequest,
                                            args=[loginCheckData[threadID], loginCheckAccountData[threadID]])
        preProcessThread.start()

    time.sleep(WAIT_TIME_MAX['isLogin'])

    print(loginConsumeTimeList)
    plt.figure(figsize=(7, 4))
    plt.xlabel("response time(s)")
    plt.ylabel("num")
    plt.title("Login Consume Time Distribute(" + str(len(loginCheckAccountData)) + ")")
    plt.hist(loginConsumeTimeList, bins=25)
    plt.show()

if TEST_PROCEDURE["isUpload"]:
    uploadNewSingleImageUrl = "http://49.232.229.126:7000/NBI/Image/upload/"
    uploadImageConsumeTimeList = []
    gidMap = {}


    def uploadNewSrcImageRequest(*args):
        startTime = time.time()
        request = Request(
            'POST',
            url=uploadNewSingleImageUrl,
            files=args[1],
            data=args[0],
        ).prepare()
        s = Session()
        response = s.send(request)

        print(response.json())
        uploadImageConsumeTimeList.append(time.time() - startTime)
        gidMap[args[0]["uid"]] = response.json()['gid']


    # upload new src image
    for threadID in range(len(loginCheckAccountData)):
        d = loginCheckAccountData[threadID]
        files = {
            'blueImage': ('1-415nm.jpg', open('./testImg/1-415nm.jpg', 'rb'), 'image/jpeg'),
            'greenImage': ('1-540nm.jpg', open('./testImg/1-540nm.jpg', 'rb'), 'image/jpeg'),
            'whiteImage': ('1-NBI.jpg', open('./testImg/1-NBI.jpg', 'rb'), 'image/jpeg'),
        }
        uploadNewSrcImageData = {
            "uid": d['uid'],
            "token": d['token'],
            "sampleName": "",
            "remark": "",
            "part": "",
            "diagnoseBefore": "",
        }
        preProcessThread = threading.Thread(target=uploadNewSrcImageRequest,
                                            args=[uploadNewSrcImageData, files])
        preProcessThread.start()

    time.sleep(WAIT_TIME_MAX["isUpload"])

    print(uploadImageConsumeTimeList)
    plt.figure(figsize=(7, 4))
    plt.xlabel("response time(s)")
    plt.ylabel("num")
    plt.title("upload New Image Time Distribute(" + str(len(loginCheckAccountData)) + ")")
    plt.hist(uploadImageConsumeTimeList, bins=25)
    plt.show()

    # 生成
    if TEST_PROCEDURE["isGenerate"]:
        getSingleImageResultUrl = "http://49.232.229.126:7000/NBI/Image/getResult/"
        getSingleImageResultTimeList = []


        def getSingleImageResultRequest(*args):
            startTime = time.time()
            request = Request(
                'POST',
                url=getSingleImageResultUrl,
                data=args[0],
            ).prepare()
            s = Session()
            response = s.send(request)

            print(response.json())
            getSingleImageResultTimeList.append(time.time() - startTime)


        for threadID in range(len(loginCheckAccountData)):
            d = loginCheckAccountData[threadID]
            getSingleImageResultRequestData = {
                "user": d['uid'],
                "token": d['token'],
                "gid": gidMap[d["uid"]],
                "channelOffset": 0,
                "brightnessAdjust": 0,
                "isAutoChannel": False,
                "isAutoBrightness": True,
                "mode": "easy",
            }
            getResultThread = threading.Thread(target=getSingleImageResultRequest,
                                               args=[getSingleImageResultRequestData])
            getResultThread.start()

        time.sleep(WAIT_TIME_MAX["isGenerate"])

        print(getSingleImageResultTimeList)
        plt.figure(figsize=(7, 4))
        plt.xlabel("response time(s)")
        plt.ylabel("num")
        plt.title("Generate and Get NBI Image Time Distribute(" + str(len(loginCheckAccountData)) + ")")
        plt.hist(getSingleImageResultTimeList, bins=25)
        plt.show()
