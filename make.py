import struct
import shutil
import os
import zipfile
from moviepy.editor import *

print('读取video')
if not os.path.exists('video'):
    print('video文件夹不存在')
    exit(0)

print('清理dist')
if os.path.exists('dist'):
    shutil.rmtree('dist')
os.mkdir('dist')
os.mkdir('dist/seq')

videoclip = None
for file in os.listdir('video'):
    if file.find('.') == 0:
        print('pass hidden file %s' % file)
        continue
    videoclip = VideoFileClip(os.path.join('video',file))
    audioclip = AudioFileClip(os.path.join('video',file))
    break

videoclip.write_images_sequence("dist/seq/frame%04d.jpg",fps=10, verbose=True)
audioclip.write_audiofile("dist/audio.wav",fps=48000,nbytes=2,codec="pcm_s16le",ffmpeg_params=['-ac','1'],verbose=True)

wavclip = open("dist/audio.wav","rb")
wavclip.seek(12)

while True:
    typeBin = wavclip.read(4)
    type,=struct.unpack('i',typeBin)
    size,=struct.unpack('i',wavclip.read(4))
    print (typeBin,size)
    if type == 1635017060:
        print ("got data chunk")
        break
    wavclip.seek(size,1)

pcm = open("dist/seq/audio.pcm","wb")
pcm.write(wavclip.read())
wavclip.close()
pcm.close()

z = zipfile.ZipFile("dist/seq.zip", 'w')
for d in os.listdir("dist/seq"):
    z.write("dist/seq" + os.sep + d, "seq" + os.sep + d)
z.close()
