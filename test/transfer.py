import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

baseDir = '/Users/wangshan/Desktop/image/xia/'

def deleteFile(basePath , key):
    files = getImg(basePath)
    for item in files:
        if key in item:
            os.remove(item)

def getImg(baseDir):
    imgs = []
    if os.path.isdir(baseDir):
        for item in os.listdir(baseDir):
            if 'jpg' in item:
                imgs.append(baseDir + item)
    return imgs


def saveResImg():
    pass

def handleImg(imgPath):
    fileName , extension = os.path.splitext(imgPath)
    img = cv2.imread(imgPath , 1)
    img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    ret , thresh = cv2.threshold(img_gray , 70 , 255 , 0)
    img_coun , img_counter = cv2.findContours(thresh , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
    img_res = cv2.drawContours(img, img_coun, -1, (0, 255, 0), 3)
    cv2.imwrite(fileName + 'de' + extension , img_res)

def boundRect(imgPath):
    fileName, extension = os.path.splitext(imgPath)
    img = cv2.imread(imgPath, 1)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 70, 255, 0)
    img_coun, img_counter = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_res = cv2.drawContours(img, img_coun, -1, (0, 255, 0), 3)
    cv2.imwrite(fileName + 'de' + extension, img_res)

def process():
    fiels = getImg(baseDir)
    for item in fiels:
        handleImg(item)

if __name__ == '__main__':
    # deleteFile(baseDir , 'de')
    process()