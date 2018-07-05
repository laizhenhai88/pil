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

if len(argv) != 3:
    print('参数不对')
    exit(0)

def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

im = Image.open(argv[1])
w,h = im.size
x = random.randint(1,w)
y = random.randint(1,h)
draw = ImageDraw.Draw(im)
draw.point((x,y),fill=rndColor())
u1 = random.randint(1,10)
u2 = random.randint(1,10)
im = im.crop((0,0,w-u1,h-u2)).convert('RGB')
im.save(argv[2])
