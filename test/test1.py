import numpy as np
import matplotlib.pyplot as plt
import cv2
import time


# img = cv2.imread('/Users/shanwang/Desktop/aa.jpeg',1)
img = cv2.imread('/Users/shanwang/Desktop/data/xia/use/train/middle/IMG_20190920_125220.jpg',1)
print(img.shape)
img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

ret , thresh = cv2.threshold(img_gray , 50 , 255 , cv2.THRESH_BINARY_INV)

kernel = np.ones((10,10),np.uint8)
img_dila = cv2.morphologyEx(thresh , cv2.MORPH_OPEN ,kernel= kernel)
# img_dila = cv2.dilate(thresh , kernel= kernel , iterations= 1)

img_coun , img_contours = cv2.findContours(img_dila , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

img_res = cv2.drawContours(img , img_coun, -1 ,  (0,255,0 ) , 3)
maxArea = 0
secondArea = 0
maxI =0
secondI = 0
for item in range(len(img_coun)):
    tempArea = cv2.contourArea(img_coun[item])
    if tempArea>maxArea:

        secondArea = maxArea
        maxArea = tempArea
        secondI = maxI
        maxI = item
        continue
    if tempArea > secondArea:
        secondArea = tempArea
        secondI = item


a = []
for j in img_coun[secondI]:
    a.append(j)
x,y,w,h = cv2.boundingRect(np.array(a))
print(x , y , w , h)
img_lun = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),30)
cv2.namedWindow('gray_src' , 0)
cv2.imshow('gray_src' , img_lun)






# plt.subplot(1,3,1)
# plt.imshow(img,'gray')
#
# plt.subplot(1,3,2)
# plt.imshow(thresh,'gray')
# plt.subplot(1,3,3)
# plt.imshow(img_lun,'gray')
# plt.show()



k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    # cv2.imwrite('/Users/wangshan/Desktop/image/bb_bak.png', img_res)
    cv2.destroyAllWindows()