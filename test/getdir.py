
import os,shutil
basePath = "/Users/shanwang/Desktop/data/xia/use/"
big = "big"
middle = "middle"
small = "small"
train = "train"
test = "test"


i = 0
for s in os.listdir(basePath + "/" + train + "/" + middle):
    if i > 1500:
        shutil.move(basePath + "/" + train + "/" + middle + "/"+s , basePath + "/" + test + "/" + middle)
        # exit()
    i = i + 1
print(i)