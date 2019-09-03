import matplotlib.pyplot as plt
import numpy as np
import csv
# plt.bar([1,3,5,7,9],[5,2,7,8,2], label="Example one")
# plt.bar([2,4,6,8,10],[8,6,2,5,6], label="Example two", color='g')
# plt.legend()
# plt.xlabel('bar number')
# plt.ylabel('bar height')
# plt.title('Epic Graph\nAnother Line! Whoa')
# plt.show()


# population_ages = [22,55,62,45,21,22,34,42,42,4,99,102,110,120,121,122,130,111,115,112,80,75,65,54,44,43,42,48]
# bins = [0,10,20,30,40,50,60,70,80,90,100,110,120,130]
# plt.hist(population_ages, bins, histtype='bar', rwidth=0.8)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
# plt.show()



# x = [1,2,3,4,5,6,7,8]
# y = [5,2,4,2,1,4,5,2]
# plt.scatter(x,y, label='skitscat', color='k', s=25, marker="o")
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
# plt.show()


# days = [1,2,3,4,5]
# sleeping = [7,8,6,11,7]
# eating =   [2,3,4,3,2]
# working =  [7,8,7,2,2]
# playing =  [8,5,7,8,13]
# plt.stackplot(days, sleeping,eating,working,playing, colors=['m','c','r','k'])
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Interesting Graph\nCheck it out')
# plt.show()


# slices = [7,2,2,13]
# activities = ['sleeping','eating','working','playing']
# cols = ['c','m','r','b']
#
# plt.pie(slices,
#         labels=activities,
#         colors=cols,
#         startangle=90,
#         shadow= True,
#         explode=(0,0.1,0,0),
#         autopct='%1.1f%%')
#
# plt.title('Interesting Graph\nCheck it out')
# plt.show()


# x = []
# y = []
# with open('aa.text','r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=',')
#     for row in plots:
#         x.append(int(row[0]))
#         y.append(int(row[1]))
#
# plt.plot(x,y, label='Loaded from file!')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
# plt.show()

# x, y = np.loadtxt('aa.text', delimiter=',', unpack=True)
# plt.plot(x,y, label='Loaded from file!')
#
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
# plt.show()


# def bytespdate2num(fmt, encoding='utf-8'):
#     strconverter = mdates.strpdate2num(fmt)
#
#     def bytesconverter(b):
#         s = b.decode(encoding)
#         return strconverter(s)
#
#     return bytesconverter
#
#
# def graph_data(stock):
#     stock_price_url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=10y/csv'
#     source_code = urllib.request.urlopen(stock_price_url).read().decode()
#     stock_data = []
#     split_source = source_code.split('\n')
#     for line in split_source:
#         split_line = line.split(',')
#         if len(split_line) == 6:
#             if 'values' not in line and 'labels' not in line:
#                 stock_data.append(line)
#
#     date, closep, highp, lowp, openp, volume = np.loadtxt(stock_data,
#                                                           delimiter=',',
#                                                           unpack=True,
#                                                           # %Y = full year. 2015
#                                                           # %y = partial year 15
#                                                           # %m = number month
#                                                           # %d = number day
#                                                           # %H = hours
#                                                           # %M = minutes
#                                                           # %S = seconds
#                                                           # 12-06-2014
#                                                           # %m-%d-%Y
#                                                           converters={0: bytespdate2num('%Y%m%d')})
#
#     plt.plot_date(date, closep, '-', label='Price')
#
#     plt.xlabel('Date')
#     plt.ylabel('Price')
#     plt.title('Interesting Graph\nCheck it out')
#     plt.legend()
#     plt.show()
#
#
# graph_data('TSLA')


# x = np.arange(1,11)
# y =  2  * x +  5
# plt.title("Matplotlib demo")
# plt.xlabel("x axis caption")
# plt.ylabel("y axis caption")
# plt.plot(x,y,"ob")
# plt.show()

# 计算正弦曲线上点的 x 和 y 坐标
# x = np.arange(0,  3  * np.pi,  0.01)
# y = np.sin(x)
# plt.title("sine wave form")
# # 使用 matplotlib 来绘制点
# plt.plot(x, y)
# plt.show()


# # 计算正弦和余弦曲线上的点的 x 和 y 坐标
# x = np.arange(0,  3  * np.pi,  0.1)
# y_sin = np.sin(x)
# y_cos = np.cos(x)
# # 建立 subplot 网格，高为 2，宽为 1
# # 激活第一个 subplot
# plt.subplot(3,  1,  1)
# # 绘制第一个图像
# plt.plot(x, y_sin)
# plt.title('Sine')
# # 将第二个 subplot 激活，并绘制第二个图像
# plt.subplot(3,  1,  2)
# plt.plot(x, y_cos)
# plt.title('Cosine')
# # 3
# plt.subplot(3,  1,  3)
# plt.plot(x, y_cos)
# plt.title('Cosine')
# # 展示图像
# plt.show()


# 创建一个 8 * 6 点（point）的图，并设置分辨率为 80
plt.figure(figsize=(8,6), dpi=80)

# 创建一个新的 1 * 1 的子图，接下来的图样绘制在其中的第 1 块（也是唯一的一块）
plt.subplot(1,1,1)

X = np.linspace(-np.pi, np.pi, 256,endpoint=True)
C,S = np.cos(X), np.sin(X)

# 绘制余弦曲线，使用蓝色的、连续的、宽度为 1 （像素）的线条
plt.plot(X, C, color="blue", linewidth=1.0, linestyle="-")

# 绘制正弦曲线，使用绿色的、连续的、宽度为 1 （像素）的线条
plt.plot(X, S, color="green", linewidth=1.0, linestyle="-")

# 设置横轴的上下限
plt.xlim(-4.0,4.0)

# 设置横轴记号
plt.xticks(np.linspace(-4,4,9,endpoint=True))

# 设置纵轴的上下限
plt.ylim(-1.0,1.0)

# 设置纵轴记号
plt.yticks(np.linspace(-1,1,5,endpoint=True))

# 以分辨率 72 来保存图片
# savefig("exercice_2.png",dpi=72)

# 在屏幕上显示
plt.show()