import numpy as np
import cv2
import matplotlib.pyplot as plt

# img = cv2.imread('/Users/wangshan/Desktop/image/putao.jpeg')
# # for i in dir(cv2):
# #     if i.startswith('COLOR_'):
# #         print(i)
#
# img_hsv = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
# lower_bule = np.array([110,50,50])
# upper_bule = np.array([130,255,255])
#
# mask = cv2.inRange(img_hsv , lower_bule , upper_bule)
#
# res = cv2.bitwise_and(img , img , mask= mask)
#
# # cv2.imshow('origin' , img)
# # cv2.imshow('mask' , mask)
# cv2.imshow('res' , res)


# green = np.uint8([[[0,255,0]]])
# hsv_green = cv2.cvtColor(green , cv2.COLOR_BGR2HSV)
# print(hsv_green)


# img = cv2.imread('/Users/wangshan/Desktop/image/putao.jpeg')
# print(img.shape)
# res = cv2.resize(img , None , fx=2 , fy=2 , interpolation=cv2.INTER_CUBIC)
# print(res.shape)
# height , width = img.shape[:2]
# res2 = cv2.resize(img , (2*width , 2 * height) , interpolation=cv2.INTER_CUBIC)
# print(res2.shape)
#
# cv2.imshow('res' , res)


# img = cv2.imread('/Users/wangshan/Desktop/image/putao.jpeg')
# rows , cols = img.shape[:2]
# M = np.float32([[1,0,100] , [0,1,50]])
# res = cv2.warpAffine(img , M , (cols-300 , rows-300))
# cv2.imshow('res' , res)


# img = cv2.imread('/Users/wangshan/Desktop/image/putao.jpeg')
# rows,cols = img.shape[:2]
# M = cv2.getRotationMatrix2D((cols/2 , rows/2) , 75 , 0.6)
# res = cv2.warpAffine(img , M,(2*cols , 2 * rows))
# cv2.imshow('res' , res)


# img = cv2.imread('/Users/wangshan/Desktop/image/putao.jpeg')
# rows , cols = img.shape[:2]
# pts1 = np.float32([[50,50],[200,50],[50,200]])
# pts2 = np.float32([[10,100],[200,50],[100,250]])
# M = cv2.getAffineTransform(pts1 , pts2)
# res = cv2.warpAffine(img , M , (cols , rows))
# cv2.imshow('res' , res)


# img = cv2.imread('/Users/wangshan/Desktop/image/putao.jpeg')
# pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
# pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
# M = cv2.getPerspectiveTransform(pts1,pts2)
# res = cv2.warpPerspective(img,M,(300,300))
#
# cv2.imshow('res' , res)


# img = cv2.imread('/Users/wangshan/Desktop/image/putao.jpeg' , 0)
# ret , thresh1 = cv2.threshold(img,127,255 , cv2.THRESH_BINARY)
# ret , thresh2 = cv2.threshold(img,127,255 , cv2.THRESH_BINARY_INV)
# ret , thresh5 = cv2.threshold(img , 127,255 , cv2.THRESH_TRUNC)
# ret , thresh3 = cv2.threshold(img , 127,255 , cv2.THRESH_TOZERO)
# ret , thresh4 = cv2.threshold(img , 127,255 , cv2.THRESH_TOZERO_INV)
# titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
# imgs = [img , thresh1 , thresh2 , thresh3 , thresh4 , thresh5]
# for i in range(6):
#     plt.subplot(2,3,i+1)
#     plt.imshow(imgs[i],'gray')
# plt.show()


# img = cv2.imread('/Users/wangshan/Desktop/image/putao.jpeg' , 0)
# ret , thresh1 = cv2.threshold(img,127,255 , cv2.THRESH_BINARY)
# thresh2= cv2.adaptiveThreshold(img , 255 , cv2.ADAPTIVE_THRESH_MEAN_C ,cv2.THRESH_BINARY , 11 , 2)
# thresh3 = cv2.adaptiveThreshold(img , 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY , 11 , 2)
# imgs = [img , thresh1 , thresh2,thresh3]
# title = ['origin' , 'binray' , 'ada men' , 'ada gaussi']
# for i in range(4):
#     plt.subplot(2,2,i+1)
#     plt.imshow(imgs[i],'gray')
# plt.show()


# img = cv2.imread('/Users/wangshan/Desktop/image/putao.jpeg' , 0)
# ret , thresh1 = cv2.threshold(img,127,255 , cv2.THRESH_BINARY)
# ret , thresh2 = cv2.threshold(img , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# blur = cv2.GaussianBlur(img , (5,5) , 0)
# ret , thresh3 = cv2.threshold(blur , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# imgs = [
#     img , 0 , thresh1 ,
#     img , 0 , thresh2,
#     blur , 0 , thresh3
# ]
# for i in range(3):
#     plt.subplot(3,3,i*3+1)
#     plt.imshow(imgs[i*3],'gray')
#     plt.subplot(3, 3, i * 3 + 2)
#     plt.hist(imgs[i*3].ravel(),256 )
#     plt.subplot(3, 3, i * 3 + 3)
#     plt.imshow(imgs[i * 3+2], 'gray')
# plt.show()

# img = cv2.imread('/Users/wangshan/Desktop/image/putao.jpeg' , 0)
# kernel = np.ones((5,5) , np.float32)/25
# res = cv2.filter2D(img , -1, kernel= kernel)
# plt.subplot(121)
# plt.imshow(img , 'gray')
# plt.subplot(122)
# plt.imshow(res , 'gray')
# plt.show()


# img = cv2.imread('/Users/wangshan/Desktop/image/putao.jpeg' , 0)
# res = cv2.blur(img , (5,5))
# plt.subplot(121)
# plt.imshow(img , 'gray')
# plt.subplot(122)
# plt.imshow(res , 'gray')
# plt.show()

# img = cv2.imread('/Users/wangshan/Desktop/image/putao.jpeg' , 0)
# # res = cv2.GaussianBlur(img , (5,5) , 0 )
# # res = cv2.medianBlur(img , 5)
# res = cv2.bilateralFilter(img , 9 , 75,75)
# plt.subplot(121)
# plt.imshow(img , 'gray')
# plt.subplot(122)
# plt.imshow(res , 'gray')
# plt.show()

# img = cv2.imread('/Users/wangshan/Desktop/image/xingtai.png' , 0)
# kernal = np.ones((5,5), np.uint8)
# res1 = cv2.erode(img , kernal , iterations=1)
# res2 = cv2.dilate(img , kernal , iterations=1)
# res3 = cv2.morphologyEx(img , cv2.MORPH_OPEN , kernal)
# res4 = cv2.morphologyEx(img , cv2.MORPH_CLOSE , kernal)
# res5 = cv2.morphologyEx(img , cv2.MORPH_GRADIENT,kernal)
# res6 = cv2.morphologyEx(img , cv2.MORPH_TOPHAT ,kernal)
# plt.subplot(231)
# plt.imshow(res1 , 'gray')
# plt.subplot(232)
# plt.imshow(res2 , 'gray')
# plt.subplot(233)
# plt.imshow(res3 , 'gray')
# plt.subplot(234)
# plt.imshow(res4 , 'gray')
# plt.subplot(235)
# plt.imshow(res5 , 'gray')
# plt.subplot(236)
# plt.imshow(res6 , 'gray')
# plt.show()


img = cv2.imread('/Users/wangshan/Desktop/image/yue3.jpeg' , 0)
laplacian = cv2.Laplacian(img , cv2.CV_64F)
sobelx = cv2.Sobel(img , cv2.CV_64F , 1,0,ksize=5)
sobely = cv2.Sobel(img , cv2.CV_64F , 0,1,ksize=5)
plt.subplot(221)
plt.imshow(img , 'gray')
plt.subplot(222)
plt.imshow(laplacian , 'gray')
plt.subplot(223)
plt.imshow(sobelx , 'gray')
plt.subplot(224)
plt.imshow(sobely , 'gray')
plt.show()



# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('s'): # wait for 's' key to save and exit
#     cv2.destroyAllWindows()