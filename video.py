# coding=utf-8
from moviepy.editor import *
import os
import shutil
import uuid
from props import readprops

# 参数设置
props = readprops('video.props')
print(props)

msg = '喜欢我就搜索 公众号ttimeinv 等你来哟~'
color = 'red'
fontsize = 70

if '话术' in props:
    msg = props['话术']
if '字体颜色' in props:
    color = props['字体颜色']
if '字体大小' in props:
    fontsize = int(props['字体大小'])

print('读取video')
if not os.path.exists('video'):
    print('video文件夹不存在')
    exit(0)

print('清理dist')
if os.path.exists('dist'):
    shutil.rmtree('dist')
os.mkdir('dist')


for file in os.listdir('video'):
    if file.find('.') == 0:
        print('pass hidden file %s' % file)
        continue
    videoclip = VideoFileClip(os.path.join('video',file))
    w,h = videoclip.size
    if len(msg) == 0:
        # 没有话术，则重构文件格式
        videoclip.to_videofile(os.path.join('dist',str(uuid.uuid4()) + '.mp4'),fps=20,codec='libx264',audio_codec='aac',ffmpeg_params=['-ac','1'],verbose=False)
        continue
    txt_clip = TextClip(msg,fontsize=fontsize,color=color,font='msyh.ttf')
    tw,th = txt_clip.size

    speed = 200
    stay = 2
    def moving(t):
        if t+stay > videoclip.duration:
            t = videoclip.duration -stay
        return (w-tw+videoclip.duration*speed-t*speed-stay*speed,'bottom')
    txt_clip = txt_clip.set_position(moving).set_duration(videoclip.duration)
    videoclip = CompositeVideoClip([videoclip, txt_clip])
    videoclip.to_videofile(os.path.join('dist',str(uuid.uuid4()) + '.mp4'),fps=20,codec='libx264',audio_codec='aac',ffmpeg_params=['-ac','1'],verbose=False)
