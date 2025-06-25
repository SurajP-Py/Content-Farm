# editing/edit.py

from moviepy import (
    ImageClip, 
    VideoFileClip,
    CompositeVideoClip, 
    AudioFileClip,
    concatenate_videoclips,
    TextClip
)
from recording import config
from games import consts
import random

audios = [
    "editing\music\morning-garden.mp3", 
    "editing\music\lofi-chill-313055.mp3", 
    "editing\music\highway-havoc.mp3", 
    "editing\music\chill-beats-323454.mp3", 
    "editing\music\chill-beats-185843.mp3", 
    "editing\music\background-music-362185.mp3"
    ]

def edit():
    footage = VideoFileClip(config.FILE_NAME)
    gameplay_footage = footage.subclipped(3, footage.duration)

    clips = []

    for i in range(config.START_DELAY):
        clips.append(CompositeVideoClip([footage.subclipped(i, i+1), TextClip(text="{}".format(config.START_DELAY - i), font_size = 100, color = consts.WHITE, size=(config.WIDTH, 200), text_align="center").with_position(("center", "center")).with_duration(1)]))

    clips.append(gameplay_footage)

    final = concatenate_videoclips(clips).with_audio(AudioFileClip(random.choice(audios)))
    final = final.subclipped(0, footage.duration)
    final.write_videofile("final_" + config.FILE_NAME)