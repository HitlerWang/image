import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

# img=cv2.imread('/Users/wangshan/Desktop/image/yue1.jpeg')
# ptx = img[100,100,2]
# print(ptx)
# print(img.shape)
# print(img.size , img.dtype)
# img.itemset((100,100,2) ,100)
# print(img.item(100,100,2))
# BLUE=[255,0,0]
# # img[:,:,2] = 0
# # img[:,:,1] = 0
# constant= cv2.copyMakeBorder(img,10,10,10,10,cv2.BORDER_CONSTANT,value=BLUE)
# cv2.imshow('aa' , constant)
# # k= cv2.waitKey(0)
# # time.sleep(3)
# # cv2.destroyAllWindows()
#
# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('s'): # wait for 's' key to save and exit
#     cv2.destroyAllWindows()


# img1=cv2.imread('/Users/wangshan/Desktop/image/yue1.jpeg')
# img2=cv2.imread('/Users/wangshan/Desktop/image/yue2.jpeg')
# print(img1.shape)
# print(img2.shape)
#
# img = cv2.addWeighted(img1 , 0.8 , img2 , 0.2 , 0)
#
# cv2.imshow('img' , img)
#
#
# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('s'): # wait for 's' key to save and exit
#     cv2.destroyAllWindows()




img1=cv2.imread('/Users/wangshan/Desktop/image/yue1.jpeg')
img2=cv2.imread('/Users/wangshan/Desktop/image/logo.png')
logorows , logocols , logochannels = img2.shape
print(img2.shape)
roi = img1[0:logorows , 0 : logocols]
img2gray = cv2.cvtColor(img2 , cv2.COLOR_BGR2GRAY)
ret , mask = cv2.threshold(img2gray , 10 , 255 , cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
img1_bg = cv2.bitwise_and(roi , roi ,mask = mask_inv)
img2_fg = cv2.bitwise_and(img2 , img2 ,mask = mask)
des = cv2.add(img1_bg , img2_fg)
img1[0:logorows , 0:logocols] = des
plt.subplot(121),plt.imshow(img1_bg,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img2_fg,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.subplot(121),plt.imshow(des,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(121),plt.imshow(img1,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.show()
e1 = cv2.getTickCount()
# your code execution
e2 = cv2.getTickCount()
time = (e2 - e1)/ cv2.getTickFrequency()
print(time)