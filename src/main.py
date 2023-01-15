"""Main"""

import os
import json
import praw
from dotenv import load_dotenv

from video_creation.thread import get_thread
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


def get_videos():
    """Gets videos for each subreddit"""

    # Create the Reddit instance
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT"),
    )

    init()

    for subreddit_dict in subreddits:
        if not os.path.exists(f"assets/subreddits/{subreddit_dict['name']}"):
            os.mkdir(f"assets/subreddits/{subreddit_dict['name']}")

        subreddit = reddit.subreddit(subreddit_dict["name"])

        # Get threads from the subreddit
        threads = subreddit.top(time_filter="day", limit=25)

        count = 0
        for thread in threads:
            subreddit_name = thread.subreddit.display_name
            thread_id = thread.id

            # Get content of thread
            thread = get_thread(thread, subreddit_dict["comments"])
            if thread is None:
                log_videos(subreddit_name, "failed", thread_id)
                continue

            # Create video of thread
            if get_video(thread) is None:
                log_videos(subreddit_name, "failed", thread_id)
                continue

            count += 1
            if count == 1:
                break


if __name__ == "__main__":
    subreddits = [{"name": "AskReddit", "comments": True}]
    get_videos()
