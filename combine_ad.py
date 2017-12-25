# coding=utf-8
from moviepy.editor import *
import os
import shutil
import uuid

print('读取combine')
if not os.path.exists('combine'):
    print('combine文件夹不存在')
    exit(0)

print('清理dist')
if os.path.exists('dist'):
    shutil.rmtree('dist')
os.mkdir('dist')

finalSize = (1080,1920)
# finalSize = (270,480)

videos = []
duration = 0
for file in os.listdir('combine'):
    if file.find('.') == 0:
        print('pass hidden file %s' % file)
        continue
    videoclip = VideoFileClip(os.path.join('combine',file), resize_algorithm = 'bilinear')
    print('ori:',videoclip.size)
    videoclip = videoclip.set_start(duration)
    videoclip = videoclip.set_position(("center","center"))
    duration += videoclip.duration
    videos.append(videoclip)

videos[-1] = videos[-1].resize(finalSize)

index = 0
for clip in videos[0:-1]:
    if clip.size[1]/clip.size[0] > finalSize[1]/finalSize[0]:
        # 说明H大，同步H
        videos[index] = clip.resize((clip.size[0]*finalSize[1]/clip.size[1],finalSize[1]))
    else:
        # 说明W大，同步W
        videos[index] = clip.resize((finalSize[0],clip.size[1]*finalSize[0]/clip.size[0]))
    index += 1


for v in videos:
    print('new:',v.size)

# logo
logoPath = None
for file in os.listdir('logo'):
    if file.find('.') == 0:
        print('pass hidden file %s' % file)
        continue
    logoPath = os.path.join('logo',file)

if logoPath is not None:
    logo = ImageClip(logoPath)
    # logo = logo.resize((200,200))
    # 右上
    logo = logo.set_position((finalSize[0] - logo.size[0] - 50, 225))
    # 右下
    # logo = logo.set_position((finalSize[0] - logo.size[0] - 50, finalSize[1] - logo.size[1] - 50))
    logo = logo.set_duration(duration - videos[-1].duration)
    videos.append(logo)

cv = CompositeVideoClip(videos, size=finalSize)
print('cv:',cv.size)
cv.to_videofile(os.path.join('dist',str(uuid.uuid4()) + '.mov'),fps=20,codec='libx264',audio_codec='aac',ffmpeg_params=['-ac','1'],verbose=False)
