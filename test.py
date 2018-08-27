from moviepy.editor import VideoClip
from moviepy.editor import ImageClip


ic = ImageClip("temp.jpg")

def make_frame(t):
    """ returns an image of the frame at time t """
    # ... create the frame with any library
    return ic.get_frame(0) # (Height x Width x 3) Numpy array

animation = VideoClip(make_frame, duration=15) # 3-second clip

# For the export, many options/formats/optimizations are supported
animation.write_videofile("my_animation.mp4", fps=1) # export as video
# animation.write_gif("my_animation.gif", fps=24)
