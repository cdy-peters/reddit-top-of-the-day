import time
import math
import json
import sys

from src.utils.log_videos import move_video
from src.video_creation.tts import TTS
from src.video_creation.background import get_subclip
from src.video_creation.create_video import create_video


def remake_video(thread):
    """Remakes the video"""

    # Get audio clips
    tts = TTS(thread["subreddit"], thread["id"])
    length = tts.get_audio(thread)

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
    move_video(thread["subreddit"], thread["id"], "pending_remake", "pending_review")


if __name__ == "__main__":
    THREAD = sys.argv[1]
    remake_video(json.loads(THREAD))
