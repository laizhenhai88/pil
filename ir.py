# coding=utf-8
import os
from sys import argv
import random
import shutil
import itertools
import uuid
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
from props import readprops

i=0
for file in os.listdir('avatar'):
    if file.find('.') == 0:
        print ('pass hidden file %s' % file)
        continue
    im = Image.open(os.path.join('avatar', file))
    im = im.resize((100,100))
    im = im.convert('RGB')
    i=i+1
    print('处理第', i, '组')
    im.save(os.path.join('avatar2', str(i) + '.jpg'), 'jpeg')
