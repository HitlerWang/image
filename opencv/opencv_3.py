import cv2
import numpy as np
from matplotlib import pyplot as plt

# img = cv2.imread('/Users/wangshan/Desktop/image/yue3.jpeg',0)
# edges = cv2.Canny(img,100,200)
# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.show()

# img = cv2.imread('/Users/wangshan/Desktop/image/yue1.jpeg',1)
# lower_res = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(img)))
# hight_res = cv2.pyrUp(cv2.pyrUp(cv2.pyrUp(img)))
# print(img.shape)
# print(lower_res.shape)
# print(hight_res.shape)
# plt.subplot(131)
# plt.imshow(img)
# plt.subplot(132)
# plt.imshow(lower_res)
# plt.subplot(133)
# plt.imshow(hight_res)
# plt.show()

img = cv2.imread('/Users/wangshan/Desktop/image/yue1.jpeg',1)
lower_res = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(img)))
res = cv2.pyrUp(cv2.pyrUp(cv2.pyrUp(lower_res)))
print(res.shape)
print(img.shape)

plt.subplot(131)
plt.imshow(img)
plt.subplot(132)
plt.imshow(res)
plt.subplot(133)
plt.imshow(img-res)
plt.show()