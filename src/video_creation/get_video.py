"""Creates the video"""

import time
import math
import json

from src.utils.log_videos import log_videos
from src.video_creation.tts import TTS
from src.video_creation.screenshots import get_screenshots
from src.video_creation.background import get_subclip
from src.video_creation.create_video import create_video


def get_video(thread):
    """Gets the video"""

    # Get audio clips
    tts = TTS(thread["subreddit"], thread["id"])
    length = tts.get_audio(thread)
    if length is None:  # The the audio is too long
        return None

    # Add length to thread
    thread["length"] = length

    # Get screenshots
    get_screenshots(thread)

    # Get background
    get_subclip(thread["subreddit"], thread["id"], length)

    # Get video
    create_video(thread)

    # Add created_at to thread
    thread["created_at"] = math.floor(time.time())

    # Add thread object to thread.json
    path = f"assets/subreddits/{thread['subreddit']}/{thread['id']}"
    with open(f"{path}/thread.json", "w", encoding="utf-8") as f:
        json.dump(thread, f)

    # Add video to videos.json
    log_videos(thread["subreddit"], "pending_review", thread["id"])

    return thread
