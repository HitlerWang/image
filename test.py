import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('/Users/wangshan/Desktop/image/yue3.jpeg',0)
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
# print(plt.xticks([]))
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
