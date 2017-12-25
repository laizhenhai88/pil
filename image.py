# coding=utf-8
import os
from sys import argv
import random
import shutil
import itertools
import uuid
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
from props import readprops

# 参数设置
props = readprops('image.props')
print(props)

msg = '更多美女请关注公众号 ttimeinv'
color = 'red'
fontsize = 36

if '话术' in props:
    msg = props['话术']
if '字体颜色' in props:
    color = props['字体颜色']
if '字体大小' in props:
    fontsize = int(props['字体大小'])

filter = ['反转','局部模糊','装饰表情','拉伸']
filterCount = 3

if filterCount > len(filter):
    print('filterCount should <= %d' % len(filter))
    exit(0)

ptt = list(itertools.permutations(filter, filterCount))
print('过滤器 %d 过滤长度 %d 排列种类 %d' % (len(filter), filterCount, len(ptt)))

print('清理dist')
if os.path.exists('dist'):
    shutil.rmtree('dist')

print('读取image')
if not os.path.exists('image'):
    print('image不存在')
    exit(0)

imgs = []
for file in os.listdir('image'):
    if file.find('.') == 0:
        print ('pass hidden file %s' % file)
        continue
    print ('构造过滤器排列 %s' % file)
    for i in range(len(ptt)):
        ri = random.randint(0, len(ptt)-1)
        ptt[i],ptt[ri] = ptt[ri],ptt[i]
    imgs += [{'file': file,'filters': ptt[:]}]

print ('创建dist文件夹')
os.mkdir('dist')

print ('读取装饰')
dec = []
for file in os.listdir('decorate'):
    dec += [Image.open(os.path.join('decorate', file))]

print ('加载字体')
font = ImageFont.truetype('msyh.ttf', fontsize)

for i in range(len(ptt)):
    print ('构造第 %d 组图片' % (i+1))
    os.mkdir(os.path.join('dist', str(i)))
    index = 0
    for imgUnit in imgs:
        index += 1
        im = Image.open(os.path.join('image', imgUnit['file']))
        # 提前旋转并裁剪，确保基础图片差异比较大
        u = random.randint(10,20)
        w,h = im.size
        im = im.rotate(1).crop((u,u,w-u,h-u))
        for f in imgUnit['filters'][i]:
            if f == '反转':
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            elif f == '局部模糊':
                w,h = im.size
                mask = im.crop((w*4//5, h*1//5, w*5//5, h*5//5)).filter(ImageFilter.BLUR).convert('RGB')
                im = im.convert('RGB')
                im.paste(mask, (w*4//5, h*1//5))
            elif f == '装饰表情':
                u = random.randint(0, len(dec) -1)
                w,h = im.size
                im = im.convert('RGBA')
                im.alpha_composite(dec[u], (w//5,h*4//5), (0,0))
            elif f == '拉伸':
                u = random.randint(10,20)
                w,h = im.size
                im = im.resize((w+u, h+u))
            else:
                print ('没有这个过滤器 %s' % f)
        im = im.convert('RGB')
        im.save(os.path.join('dist', str(i), str(uuid.uuid4()) + '.jpg'), 'jpeg')
        if index == len(imgs):
            print ('构造广告')
            w,h = im.size
            ad = Image.new('RGB', (w,fontsize+10), (255, 255, 255))
            draw = ImageDraw.Draw(ad)
            tw,th = draw.textsize(msg, font=font)
            draw.text(((w-tw)//2,(fontsize+10-th)//2), msg, font=font, fill=ImageColor.getcolor('red', 'RGB'), align='center')
            im.paste(ad, (0, h-fontsize-10))
            im.save(os.path.join('dist', str(i), 'ad.jpg'), 'jpeg')
