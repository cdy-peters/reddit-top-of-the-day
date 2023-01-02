"""Handles the background for videos"""

import os
import random
from moviepy.editor import VideoFileClip


def get_subclip(id, length):
    """Gets a background for the video"""

    backgrounds = os.listdir("assets/backgrounds")
    background = VideoFileClip(f"assets/backgrounds/{random.choice(backgrounds)}")

    start = random.randint(0, int(background.duration - length))

    background.subclip(start, start + length).write_videofile(
        f"assets/threads/{id}/background.mp4"
    )
