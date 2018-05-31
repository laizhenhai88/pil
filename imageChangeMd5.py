# coding=utf-8
# 这个版本随机裁剪一部分数据，使得md5值变化
import os
from sys import argv
import random
import shutil
import itertools
import uuid
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
from props import readprops


print('清理dist')
if os.path.exists('dist'):
    shutil.rmtree('dist')

print ('创建dist文件夹')
os.mkdir('dist')

print('读取image')
if not os.path.exists('image'):
    print('image不存在')
    exit(0)

def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

for file in os.listdir('image'):
    if file.find('.') == 0:
        print ('pass hidden file %s' % file)
        continue
    im = Image.open(os.path.join('image', file))
    w,h = im.size
    x = random.randint(1,w)
    y = random.randint(1,h)
    draw = ImageDraw.Draw(im)
    draw.point((x,y),fill=rndColor())
    u1 = random.randint(1,10)
    u2 = random.randint(1,10)
    im = im.crop((0,0,w-u1,h-u2)).convert('RGB')
    im.save(os.path.join('dist', file))
