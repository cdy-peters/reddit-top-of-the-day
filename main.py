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
        obj = {"pending": {}, "approved": {}, "deleted": {}}

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
        thread = get_thread(thread)

        if thread is None:
            continue

        # Get audio clips
        tts = TTS(thread["subreddit"], thread["id"])
        length = tts.get_audio(thread)
        if length is None:  # The the audio is too long
            continue

        # Get screenshots
        get_screenshots(thread)

        # Get background
        get_subclip(thread["subreddit"], thread["id"], length)

        # Get video
        get_video(thread)

        # Add thread object to thread.json
        path = f"assets/subreddits/{thread['subreddit']}/{thread['id']}"
        with open(f"{path}/thread.json", "w", encoding="utf-8") as f:
            json.dump(thread, f)

        # Add video to videos.json
        with open("data/videos.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        pending = data["pending"]
        if thread["subreddit"] not in pending:
            pending[thread["subreddit"]] = []
        pending[thread["subreddit"]].append(thread["id"])

        with open("data/videos.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

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

    subreddits = ["AmItheAsshole"]
    for subreddit in subreddits:
        if not os.path.exists(f"assets/subreddits/{subreddit}"):
            os.mkdir(f"assets/subreddits/{subreddit}")

        subreddit = reddit.subreddit(subreddit)
        main()
