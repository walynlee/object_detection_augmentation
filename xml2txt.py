
import os
import xml.etree.ElementTree as ET
from decimal import Decimal
 
dirpath = 'aug_xml'  # 原来存放xml文件的目录

newdir = 'aug_txt'  # 修改label后形成的txt目录
 
if not os.path.exists(newdir):
    os.makedirs(newdir)
 
for fp in os.listdir(dirpath):
 
    root = ET.parse(os.path.join(dirpath, fp)).getroot()
 
    xmin, ymin, xmax, ymax = 0, 0, 0, 0
    sz = root.find('size')
    width = float(sz[0].text)
    height = float(sz[1].text)
    filename = root.find('filename').text
    print(fp)
    with open(os.path.join(newdir, fp.split('.')[0] + '.txt'), 'a+') as f:
        for child in root.findall('object'):  # 找到图片中的所有框
 
            sub = child.find('bndbox')  # 找到框的标注值并进行读取
            sub_label = child.find('name')
            xmin = float(sub[0].text)
            ymin = float(sub[1].text)
            xmax = float(sub[2].text)
            ymax = float(sub[3].text)
            try:  # 转换成yolov的标签格式，需要归一化到（0-1）的范围内
                x_center = Decimal(str(round(float((xmin + xmax) / (2 * width)),6))).quantize(Decimal('0.000000'))
                y_center = Decimal(str(round(float((ymin + ymax) / (2 * height)),6))).quantize(Decimal('0.000000'))
                w = Decimal(str(round(float((xmax - xmin) / width),6))).quantize(Decimal('0.000000'))
                h = Decimal(str(round(float((ymax - ymin) / height),6))).quantize(Decimal('0.000000'))
                print(str(x_center) + ' ' + str(y_center)+ ' '+str(w)+ ' '+str(h))
                #读取需要的标签
                #if sub_label.text == 'armor':
                f.write(' '.join([str(0), str(x_center), str(y_center), str(w), str(h) + '\n']))

            except ZeroDivisionError:
                print(' width有问题')
            '''有其他标签选用
                            if sub_label.text == 'xxx':
                                f.write(' '.join([str(1), str(x_center), str(y_center), str(w), str(h) + '\n']))
                            if sub_label.text == 'xxx':
                                f.write(' '.join([str(2), str(x_center), str(y_center), str(w), str(h) + '\n']))'''
            # with open(os.path.join(newdir, fp.split('.')[0] + '.txt'), 'a+') as f:
            #     f.write(' '.join([str(2), str(x_center), str(y_center), str(w), str(h) + '\n']))
