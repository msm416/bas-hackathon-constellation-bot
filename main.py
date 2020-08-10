import facebook
import os
import random
import cv2
import numpy as np
from collections import deque
import math


def upload_photo(photoName):
    access_token = os.environ['FB_TOKEN_BAS']

    #here goes your access token from http://maxbots.ddns.net/token
    graph = facebook.GraphAPI(access_token)
    msg = 'Hello facebook! This is my first bot made with Python!' #message for the post
    comment_msg = 'This is a bot posted comment!' #message for the comment
    post_id = graph.put_photo(image = open(photoName, 'rb'), message= msg)["post_id"] #photo got posted!
    print('Photo has been uploaded to facebook!')
    graph.put_comment(object_id = post_id, message = comment_msg)#comment got posted!


def getClusters(edges):
    testArr = np.copy(edges)
    squareSize = 21
    n, m = testArr.shape
    for i in range(n//squareSize):
        for j in range(m//squareSize):
            nbWhitePixels = 0
            xAvg, yAvg = 0, 0
            for k in range(squareSize):
                for l in range(squareSize):
                    if(testArr[i * squareSize + k][j * squareSize + l] >= 200):
                        nbWhitePixels += 1
                        testArr[i * squareSize + k][j * squareSize + l] = 0

                        xAvg += k
                        yAvg += l

            starRadius = int(math.sqrt(nbWhitePixels)) + 2
            if(starRadius < 3):
                continue

            xAvg = xAvg // nbWhitePixels
            yAvg = yAvg // nbWhitePixels

            for k in range(- starRadius//2, starRadius//2):
                for l in range(- starRadius//2, starRadius//2):
                    if(abs(k) + abs(l) < starRadius//2):
                        testArr[i * squareSize + (xAvg) + k][j * squareSize + (yAvg) + l] = 255
    return testArr


def generateAndPost():
    constPath = "images/toBeConstellation/"
    bckgrPath = "images/backgroundSky/"

    constl = cv2.imread(constPath + random.choice(os.listdir(constPath)), 0)
    bckgr = cv2.imread(bckgrPath + random.choice(os.listdir(bckgrPath)))

    # constl = cv2.imread(constPath + 'monkey.jpg', 0)
    # bckgr = cv2.imread(bckgrPath + 'space1.jpg')

    rowsConst, colsConst = constl.shape
    rowsBckgr, colsBckgr = bckgr.shape[:2]

    resConst = cv2.resize(constl, dsize=(min(colsBckgr, colsConst * rowsBckgr // 3 // rowsConst), rowsBckgr//3), interpolation=cv2.INTER_CUBIC)

    edges = getClusters(cv2.Canny(resConst,150,150))

    # rows are fixed for resized Constellation; now we choose where to put the Constellation

    offsetCol = int(random.random() * (colsBckgr - resConst.shape[1]))

    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if edges[i][j] == 255:
                bckgr[i][j + offsetCol] = 255

    cv2.imwrite("output.jpg", bckgr)
    upload_photo("output.jpg")


if __name__ == '__main__':
    generateAndPost()

