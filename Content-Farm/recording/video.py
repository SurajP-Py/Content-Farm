# recording/video.py

# Complete credit to Dubious Code:
#  - https://www.youtube.com/@dubiouscode4802
#  - https://www.youtube.com/watch?v=JJlut7N4x7Q

import pygame,sys,os
from recording import config
from pathlib import Path
import subprocess
 
class Video:
 
    def __init__(self,size):
        self.path = Path(__file__).parent / "pngs"
        self.name = "capture"
        self.cnt = 0

        # Create folder if it doesn't exist
        self.path.mkdir(parents=True, exist_ok=True)

        # Clear out existing .png files
        for file in self.path.glob("*.png"):
            try:
                file.unlink()
            except PermissionError:
                print(f"Could not delete {file}, possibly in use.")
    
    def make_png(self,screen):
        self.cnt+=1
        fullpath = self.path / f"{self.name}{self.cnt:08d}.png"
        pygame.image.save(screen, str(fullpath))

    def make_mp4(self):
        ffmpeg_path = config.FFMPEG_BIN

        input_pattern = str(self.path / f"{self.name}%08d.png")
        output_video = config.FILE_NAME

        cmd = [
            ffmpeg_path,
            "-r", str(config.FPS),
            "-i", input_pattern,
            "-vcodec", "mpeg4",
            "-q:v", "0",
            "-y",
            output_video
        ]

        subprocess.run(cmd, check=True)