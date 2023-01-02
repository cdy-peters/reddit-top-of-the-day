"""Handles the background for videos"""

import os
import random
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# TODO: Be able to download backgrounds


def get_subclip(thread_id, length):
    """Gets a background for the video"""

    backgrounds = os.listdir("assets/backgrounds")
    background = VideoFileClip(f"assets/backgrounds/{random.choice(backgrounds)}")

    start = random.randint(0, int(background.duration - length))

    ffmpeg_extract_subclip(
        f"assets/backgrounds/{random.choice(backgrounds)}",
        start,
        start + length,
        targetname=f"assets/threads/{thread_id}/background.mp4",
    )
