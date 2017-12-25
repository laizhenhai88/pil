# coding=utf-8
from moviepy.editor import *
import os
import shutil
import uuid
from movRe import *

print('读取 reformat')
if not os.path.exists('reformat'):
    print('reformat 文件夹不存在')
    exit(0)

print('清理dist')
if os.path.exists('dist'):
    shutil.rmtree('dist')
os.mkdir('dist')

finalSize = (1080,1920)
for file in os.listdir('reformat'):
    if file.find('.') == 0:
        print('pass hidden file %s' % file)
        continue
    videoclip = VideoFileClip(os.path.join('reformat',file), resize_algorithm = 'bilinear')
    videoclip = videoclip.set_position(("center","center"))
    print('ori:',videoclip.size)
    # videoclip = videoclip.resize(finalSize)
    if videoclip.size[1]/videoclip.size[0] > finalSize[1]/finalSize[0]:
        # 说明H大，同步H
        videoclip = videoclip.resize((videoclip.size[0]*finalSize[1]/videoclip.size[1],finalSize[1]))
    else:
        # 说明W大，同步W
        videoclip = videoclip.resize((finalSize[0],videoclip.size[1]*finalSize[0]/videoclip.size[0]))
    print('new:',videoclip.size)
    videoclip = CompositeVideoClip([videoclip], size=finalSize)
    tempFile = str(uuid.uuid4()) + '.mov'
    videoclip.write_videofile('dist/'+tempFile,fps=30,codec='libx264',audio_codec='aac',ffmpeg_params=['-ac','1'],verbose=False)
