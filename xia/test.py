import cv2
import os,shutil
import random
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

maxwidth_path = ""
maxheight_path = ""
max_width = 0
max_hight = 0
tempI = 0
basePath = "/Users/shanwang/Desktop/data/xia/use/"
big = "big/"
middle = "middle/"
small = "small/"
train = "train/"
test = "test/"
qiege = "qiege/"

trainPath = basePath + train
testPath = basePath + test
qiegePath = basePath + train +qiege

qiegeImg = "3_999.jpeg"
img1 = "IMG_20190930_141241.jpg"
img2 = "IMG_20190914_143027.jpg"
img3 = "IMG_20191012_132530.jpg"
bigImgPath = basePath + train + big + img1
middlePath = basePath + train + middle + img2
smallPath = basePath + train + small + img3

def getAllImgPath(path):
    ret = []
    for item in os.listdir(path):
        if not item.endswith(".jpg"):
            continue
        ret.append(path + item)
    return ret

def hist(path):
    img = cv2.imread(path)
    print(img.shape)
    plt.hist(img.ravel(),256,[0,256]);
    plt.show()

def thresd(path):
    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

    ret , thresh1 = cv2.threshold(img , 60 , 255 , cv2.THRESH_BINARY_INV)
    ret , thresh2 = cv2.threshold(img , 60 , 255 , cv2.THRESH_BINARY)
    ret , thresh3 = cv2.threshold(img , 60 , 255 , cv2.THRESH_MASK)
    ret , thresh4 = cv2.threshold(img , 60 , 255 , cv2.THRESH_TRUNC)
    ret , thresh5 = cv2.threshold(img , 60 , 255 , cv2.THRESH_TOZERO)
    ret , thresh6 = cv2.threshold(img , 60 , 255 , cv2.THRESH_TOZERO_INV)

    plt.subplot(2,3,1)
    plt.imshow(thresh1)

    plt.subplot(2,3,2)
    plt.imshow(thresh2)

    plt.subplot(2,3,3)
    plt.imshow(img)

    plt.subplot(2,3,4)
    plt.imshow(thresh4)

    plt.subplot(2,3,5)
    plt.imshow(thresh5)

    plt.subplot(2,3,6)
    plt.imshow(thresh6)
    plt.show()


def test():
    bigImg = cv2.imread(middlePath)
    print(bigImg[100,100])
    b, g, r = cv2.split(bigImg)
    print(b[100,100])
    print(g[100,100])
    print(r[100,100])
    cv2.imshow("origin" , r)
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()
    else:
        cv2.destroyAllWindows()


def convertTensor():
    a = np.array([[1,2,3],[4,5,6],[7,8,9]])
    print(a)
    b = tf.constant(a)
    with tf.Session() as sess:
        print(b)
        for x in b.eval():
            print(x)
        print("a",a)
        tensor_a = tf.convert_to_tensor(a)
        print(tensor_a)

def imgResize(path):
    print(path)
    img = cv2.imread(path)
    print(img.shape)

    dst=cv2.resize(img,(0,0),fx=1/10,fy=1/10,interpolation=cv2.INTER_LINEAR)
    #将源图像的大小变为512*512
    # dst=cv2.resize(img,(512,512))


    cv2.namedWindow('gray_src' , 0)
    cv2.imshow('gray_src' , dst)
    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
    elif k == ord('s'): # wait for 's' key to save and exit
        # cv2.imwrite('/Users/wangshan/Desktop/image/bb_bak.png', img_res)
        cv2.destroyAllWindows()


def checkImg(path):
    guifan = 2383
    img = cv2.imread(path)
    height , width , _ = img.shape
    img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    ret , thresh = cv2.threshold(img_gray , 50 , 255 , cv2.THRESH_BINARY_INV)
    kernel = np.ones((10,10),np.uint8)
    # img_dila = cv2.morphologyEx(thresh , cv2.MORPH_OPEN ,kernel= kernel)
    img_dila = cv2.dilate(thresh , kernel= kernel , iterations= 1)
    img_coun , img_contours = cv2.findContours(img_dila , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    # img_res = cv2.drawContours(img , img_coun, -1 ,  (0,255,0 ) , 3)
    contourArea = []
    for item in range(len(img_coun)):
        contourArea.append([item , cv2.contourArea(img_coun[item])/1])
    def sortKey(elem):
        return elem[1]
    contourArea.sort(reverse=True ,key=sortKey)
    x = 0
    y  =0
    w=0
    h=0
    for i in contourArea:
        a=[]
        for j in img_coun[i[0]]:
            a.append(j)
        x,y,w,h = cv2.boundingRect(np.array(a))
        if x == 0 or y ==0 or y+h==height or x+w==width:
            print(path)
            continue
        else:
            break
    print(x,y,w,h)
    global max_width
    global max_hight
    global maxheight_path
    global maxwidth_path
    if w > max_width:
        max_width = w
        maxwidth_path = path
    if h > max_hight:
        max_hight = h
        maxheight_path = path
    if x ==0 or y==0:
        print(path)
    global tempI
    tempI = tempI + 1
    fileName = '1_' + str(tempI) + '.jpeg'
    if x + guifan > width:
        x = width - guifan
    if y + guifan > height:
        y = height - guifan
    resImg = img[y:y+guifan ,x:x+guifan]
    cv2.imwrite('/Users/shanwang/Desktop/data/xia/use/train/qiege/'+fileName,resImg)
    # img_lun = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),30)
    # cv2.namedWindow('gray_src' , 0)
    # cv2.imshow('gray_src' , img_lun)
    # k = cv2.waitKey(0)
    # if k == 27:         # wait for ESC key to exit
    #     cv2.destroyAllWindows()
    # elif k == ord('s'): # wait for 's' key to save and exit
    #     # cv2.imwrite('/Users/wangshan/Desktop/image/bb_bak.png', img_res)
    #     cv2.destroyAllWindows()

def slipImg(path , x , y , w , h ):
    # 读取要被切割的图片
    img = cv2.imread(path)
    # 要被切割的开始的像素的高度值
    beH = y
    # 要被切割的结束的像素的高度值
    hEnd = y+h
    # 要被切割的开始的像素的宽度值
    beW = x
    # 要被切割的结束的像素的宽度值
    wLen = x+w
    # 对图片进行切割
    dstImg = img[beH:hEnd,beW:wLen]
    # 展示切割好的图片
    cv2.namedWindow('dstImg' , 0)
    cv2.imshow("dstImg",dstImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    imgResize(qiegePath + qiegeImg)
    rand = random.randint(1,1500)
    # slipImg("/Users/shanwang/Desktop/data/xia/use/train/middle/IMG_20190920_123211.jpg" , 1096,1673 ,1395,2170)
    # checkImg("/Users/shanwang/Desktop/data/xia/use/train/middle/IMG_20190920_123211.jpg")
    # for item in getAllImgPath(trainPath + small):
    #     checkImg(item)
    # print("max_width : " ,max_width)
    # print("max_hight : " ,max_hight)
    # print("max_widthpath : " ,maxwidth_path)
    # print("max_hightpath : " ,maxheight_path)

    # getAllImgPath(trainPath + small)
    # test()
    # hist(bigImgPath)
    # thresd(smallPath)
    # convertTensor()

