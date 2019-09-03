import numpy as np
import cv2
import matplotlib.pyplot as plt

# img = cv2.imread('/Users/wangshan/Desktop/image/yue1.jpeg',1)
# img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
# ret , thresh = cv2.threshold(img_gray , 127 , 255 , 0 )
# img_coun , img_contours  = cv2.findContours(thresh , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
# print(img_contours)
# print(img_coun)
# img_res = cv2.drawContours(img , img_coun , -1 ,  (0,255,0 ) , 3)
# print(img_res)
# img_res = cv2.drawContours(img , img_coun , 3 ,  (0,255,0 ) , 3)
#
# cv2.imshow('aa' , img_res)


# img = cv2.imread('/Users/wangshan/Desktop/image/yue1.jpeg',0)
# ret , thresh = cv2.threshold(img , 127,255,0)
# contours , hierarchy = cv2.findContours(thresh , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
# cnt = contours[0]
# M = cv2.moments(cnt)
# area = cv2.contourArea(cnt)
# hull = cv2.convexHull(cnt)
# k = cv2.isContourConvex(cnt)
# x,y,w , h =cv2.boundingRect(cnt)
# rect = cv2.minAreaRect(cnt)
# box = cv2.boxPoints(cnt)
# box = np.int0(box)
# im = cv2.drawContours(img , box , 0 , (0,0,255) ,  2)
# (x,y) , radius = cv2.minEnclosingCircle(cnt)
# center = (int(x) , int(y))
# radius = int(radius)
# img = cv2.circle(int , center , radius , (0,255,0) , 2)
# ellipse = cv2.fitEllipse(cnt)
# img = cv2.ellipse(img, ellipse , (0,255,0) , 2)
# [vx , vy , x , y] = cv2.fitLine(cnt , cv2.DIST_L2 , 0 ,0 ,0.01 ,0.01)
# lefty = int((-x*vy/vx) + y)
# rows , cols = img.shape[:2]
# righty = int(((cols- x)*vy / vx) + y)
# img = cv2.line(img , (cols-1 , righty),(0 , lefty) , (0 ,255,0 ),2)
# leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
# rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
# topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
# bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
# img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
# perimeter = cv2.arcLength(cnt , True)
# epsilon = 0.1 * cv2.arcLength(cnt , True)
# approx = cv2.approxPolyDP(cnt , epsilon)
# print(M)
# print(cnt)

# img = cv2.imread('/Users/wangshan/Desktop/image/yue1.jpeg',1)
# hist = cv2.calcHist([img] , [0] , None , [256] , [0,256] , )
# plt.hist(img.ravel() , 256 , [0,256] )
# plt.show()
# color = ('b' , 'g' , 'r')
# for i , col in enumerate(color):
#     hitStr = cv2.calcHist([img] , [0] , None , [256] , [0,256] , )
#     plt.plot(hitStr , color=col)
# plt.xlim([0,256])
# plt.show()



img = cv2.imread('/Users/wangshan/Desktop/image/yue1.jpeg',0)
hist, bins = np.histogram(img.flattern() , 256 , [0,256])
cdf = hist.cumsum()
cdf_normalized = cdf * hist.max() / cdf.max()
plt.plot(cdf_normalized , color = 'b')
plt.hist(img.flattern() , 256 , [0,256] , color='r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.show()


# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('s'): # wait for 's' key to save and exit
#     cv2.destroyAllWindows()