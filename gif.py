# coding=utf-8
from moviepy.editor import *
from sys import argv
import os
import shutil
import uuid
from props import readprops

# 参数设置
props = readprops('gif.props')
print(props)

msg = '关注公众号 ttimeinv'
color = 'red'
fontsize = 30

if '话术' in props:
    msg = props['话术']
if '字体颜色' in props:
    color = props['字体颜色']
if '字体大小' in props:
    fontsize = int(props['字体大小'])

txt_clip = TextClip(msg,fontsize=fontsize,color=color,font='msyh.ttf')
fw,fh = txt_clip.size

print('读取gif')
if not os.path.exists('gif'):
    print('gif文件夹不存在')
    exit(0)

print('清理dist')
if os.path.exists('dist'):
    shutil.rmtree('dist')
os.mkdir('dist')

index = -1
for file in os.listdir('gif'):
    if file.find('.') == 0:
        print('pass hidden file %s' % file)
        continue
    videoclip = VideoFileClip(os.path.join('gif',file))
    w,h = videoclip.size
    if fw > w or fh > h:
        print('字体太大 或 文字太长 放弃处理：%s' % file)
        continue
    index += 1
    print('开始处理第%d个：%s' % (index+1,file))
    os.mkdir(os.path.join('dist', str(index)))
    unit = (w-fw) / 9
    for i in range(9 + 1):
        txt_clip = txt_clip.set_position((i*unit,'bottom')).set_start(0).set_duration(videoclip.duration)
        video = CompositeVideoClip([videoclip, txt_clip])
        video.write_gif(os.path.join('dist', str(index), str(uuid.uuid4()) + '.gif'), fps=8, verbose=False)
