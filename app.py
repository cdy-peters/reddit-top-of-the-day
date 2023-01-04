"""Main"""

import os
import json
import praw
from dotenv import load_dotenv

from video_creation.thread import get_thread
from video_creation.tts import get_audio
from video_creation.screenshots import get_screenshots
from video_creation.background import get_subclip
from video_creation.video import get_video

load_dotenv()


def init():
    """Initializes the program"""

    if not os.path.exists("assets"):
        os.mkdir("assets")

    if not os.path.exists("assets/subreddits"):
        os.mkdir("assets/subreddits")

    if not os.path.exists("assets/backgrounds"):
        os.mkdir("assets/backgrounds")


def main():
    """Main function"""

    # Get the thread
    threads = subreddit.top(time_filter="day", limit=25)

    count = 0

    for thread in threads:
        thread = get_thread(thread)

        if thread is None:
            continue

        # Get audio clips
        length = get_audio(thread)

        # Get screenshots
        get_screenshots(thread)

        # Get background
        get_subclip(thread["subreddit"], thread["id"], length)

        # Get video
        get_video(thread)

        # Add thread to json file
        path = f"assets/subreddits/{thread['subreddit']}/{thread['id']}"
        with open(f"{path}/thread.json", "w", encoding="utf-8") as f:
            json.dump(thread, f)

        count += 1
        if count == 1:
            break


# Create the Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT"),
)
subreddits = ["AmItheAsshole"]

init()

for subreddit in subreddits:
    if not os.path.exists(f"assets/subreddits/{subreddit}"):
        os.mkdir(f"assets/subreddits/{subreddit}")

    subreddit = reddit.subreddit(subreddit)
    main()
