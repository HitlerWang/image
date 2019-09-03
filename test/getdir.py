
import os
path = '/Users/wangshan/Desktop/image/xia/'
flag = os.path.isdir(path)
i = 0
if flag:
    for s in os.listdir(path):
        if 'jpg' in s:
            os.rename(path + s , path + 'xia_' + str(i)+'.jpg' )
            # print(path + 'xia_' + str(i)+'.jpg' )
            i = i + 1
print(flag)
