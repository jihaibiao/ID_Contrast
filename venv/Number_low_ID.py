# -*- coding = utf-8 -*-
# @Time : 2022/8/25 21:13
# @Author : 计海彪
# @File : Number.py
# @Software : PyCharm
import os,csv,random,math,numpy


if not os.path.exists('number_file'):
    os.mkdir('number_file')
data_file = open('number_file/'+'number_low'+'.csv','w',encoding='UTF-8',newline='')
writer = csv.writer(data_file)
writer.writerow(["X","Y","WIDTH","distance","ID"])
#生成点的范围
x_min = 2
x_max = 15.2
y_min = 2
y_max = 11

d = 2
ID = 2
w = 1

i = 1
x_pre = 2
y_pre = 2
while i <= 31:
    x =  round(random.uniform(x_pre-2,x_pre+2),3)
    if x_min < x < x_max:
        y_p = round(y_pre + math.sqrt(4-numpy.square(x-x_pre)),3)
        y_n = round(y_pre - math.sqrt(4 - numpy.square(x - x_pre)),3)
        y = random.choice([y_n,y_p])
        if y_min < y < y_max:
            writer.writerow([x, y, w, d, ID])
            x_pre = x
            y_pre = y
            i += 1
