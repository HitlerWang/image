import numpy as np
import matplotlib.pyplot as plt
import cv2
import time

img = cv2.imread('/Users/wangshan/Desktop/image/xia/xia_8.jpg',1)
img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

ret , thresh = cv2.threshold(img_gray , 50 , 255 , cv2.THRESH_BINARY_INV)

kernel = np.ones((10,10),np.uint8)
img_dila = cv2.dilate(thresh , kernel= kernel , iterations= 1)

img_coun , img_contours = cv2.findContours(img_dila , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
img_res = cv2.drawContours(img , img_coun, -1 ,  (0,255,0 ) , 3)

a = []
for item in img_coun:
    for j in item:
        a.append(j)
x,y,w,h = cv2.boundingRect(np.array(a))
img_lun = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow('aa' , img_lun)



k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    # cv2.imwrite('/Users/wangshan/Desktop/image/bb_bak.png', img_res)
    cv2.destroyAllWindows()