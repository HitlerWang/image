import cv2
import os,shutil
import matplotlib.pyplot as plt
basePath = "/Users/shanwang/Desktop/data/xia/use/"
big = "big/"
middle = "middle/"
small = "small/"
train = "train/"
test = "test/"

trainPath = basePath + train
testPath = basePath + test

img1 = "IMG_20190930_141241.jpg"
img2 = "IMG_20190914_143027.jpg"
img3 = "IMG_20191012_132530.jpg"
bigImgPath = basePath + train + big + img1
middlePath = basePath + train + middle + img2
smallPath = basePath + train + small + img3

def getAllImgPath(path):
    for item in os.listdir(path):
        img = cv2.imread(path + item)
        print(img[100,100])

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


if __name__ == '__main__':
    # getAllImgPath(trainPath + small)
    # test()
    hist(bigImgPath)
    # thresd(smallPath)
