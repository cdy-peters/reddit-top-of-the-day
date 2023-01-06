"""Main"""

import os
import json
import praw
from dotenv import load_dotenv

from video_creation.thread import get_thread
from video_creation.tts import TTS
from video_creation.screenshots import get_screenshots
from video_creation.background import get_subclip
from video_creation.video import get_video

from utils.log_videos import log_videos

load_dotenv()


def init():
    """Initializes the program"""

    if not os.path.exists("assets"):
        os.mkdir("assets")

    if not os.path.exists("assets/backgrounds"):
        os.mkdir("assets/backgrounds")

    if not os.path.exists("assets/subreddits"):
        os.mkdir("assets/subreddits")

    if not os.path.exists("assets/approved"):
        os.mkdir("assets/approved")

    # Stores the subreddit and thread id of produced videos
    if not os.path.exists("data/videos.json"):
        obj = {
            "pending_review": {},
            "pending_remake": {},
            "pending_upload": {},
            "uploaded": {},
            "deleted": {},
            "failed": {},
        }

        with open("data/videos.json", "w", encoding="utf-8") as f:
            json.dump(obj, f)

    # Stores Reddit authentication state
    if not os.path.exists("data/state.json"):
        with open("data/state.json", "w", encoding="utf-8") as f:
            json.dump({}, f)


def main():
    """Main function"""

    # Get the thread
    threads = subreddit.top(time_filter="day", limit=25)

    count = 0

    for thread in threads:
        subreddit_name = thread.subreddit.display_name
        thread_id = thread.id

        thread = get_thread(thread)
        if thread is None:
            log_videos(subreddit_name, "failed", thread_id)
            continue

        # Get audio clips
        tts = TTS(subreddit_name, thread_id)
        length = tts.get_audio(thread, subreddit_dict["comments"])
        if length is None:  # The the audio is too long
            log_videos(subreddit_name, "failed", thread_id)
            continue

        # Get screenshots
        get_screenshots(thread)

        # Get background
        get_subclip(subreddit_name, thread_id, length)

        # Get video
        get_video(thread)

        # Add thread object to thread.json
        path = f"assets/subreddits/{subreddit_name}/{thread_id}"
        with open(f"{path}/thread.json", "w", encoding="utf-8") as f:
            json.dump(thread, f)

        # Add video to videos.json
        log_videos(subreddit_name, "pending_review", thread_id)

        count += 1
        if count == 1:
            break


if __name__ == "__main__":
    # Create the Reddit instance
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT"),
    )

    init()

    subreddits = [{"name": "AskReddit", "comments": True}]
    for subreddit_dict in subreddits:
        if not os.path.exists(f"assets/subreddits/{subreddit_dict['name']}"):
            os.mkdir(f"assets/subreddits/{subreddit_dict['name']}")

        subreddit = reddit.subreddit(subreddit_dict["name"])
        main()
