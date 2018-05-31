# coding=utf-8
# 这个版本随机裁剪一部分数据，使得md5值变化
import os
from sys import argv
import random
import shutil
import itertools
import uuid
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
from moviepy.editor import *
import os
import shutil
import uuid
import math


print('清理dist')
if os.path.exists('dist'):
    shutil.rmtree('dist')

print ('创建dist文件夹')
os.mkdir('dist')

print('读取video')
if not os.path.exists('video'):
    print('video不存在')
    exit(0)


for file in os.listdir('video'):
    if file.find('.') == 0:
        print ('pass hidden file %s' % file)
        continue
    videoclip = VideoFileClip(os.path.join('video',file), resize_algorithm = 'bilinear')
    # txt_clip = txt_clip.set_position((200,'bottom')).set_duration(videoclip.duration)
    u1 = random.randint(1,10)
    u2 = random.randint(1,10)
    saveSize = videoclip.size
    videoclip = videoclip.crop(x1=u1,y1=u1,x2=saveSize[0]-u1-u2,y2=saveSize[1]-u1-u2).resize(saveSize)
    txt_clip = TextClip('.',fontsize=5,color='white',font='msyh.ttf')
    txt_clip = txt_clip.set_position((random.randint(1,videoclip.size[0]),'bottom')).set_duration(random.randint(1,math.floor(videoclip.duration)))
    videoclip = CompositeVideoClip([videoclip, txt_clip], size=saveSize)
    videoclip.write_videofile(os.path.join('dist', file),fps=30,codec='libx264',audio_codec='aac',ffmpeg_params=['-ac','1'],verbose=False)
