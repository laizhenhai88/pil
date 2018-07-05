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

if len(argv) != 4:
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

msg = argv[3]
w,h = im.size
fontsize = 20
font = ImageFont.truetype('msyh.ttf', fontsize)
tw,th = draw.textsize(msg, font=font)

ad = Image.new('RGB', (w,fontsize+10), (255, 255, 255))
draw = ImageDraw.Draw(ad)
draw.text(((w-tw)//2,(fontsize+10-th)//2), msg, font=font, fill=ImageColor.getcolor('red', 'RGB'), align='center')
im.paste(ad, (0, h-fontsize-10))

# draw = ImageDraw.Draw(im)
# draw.text(((w-tw)//2,h-fontsize-10), msg, font=font, fill=ImageColor.getcolor('red', 'RGB'), align='center')

im.save(argv[2])
