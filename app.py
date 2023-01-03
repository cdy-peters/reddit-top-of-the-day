"""Main"""

import os
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
    thread = get_thread(subreddit)

    # Get audio clips
    length = get_audio(thread)

    # Get screenshots
    get_screenshots(thread)

    # Get background
    get_subclip(thread["subreddit"], thread["id"], length)

    # Get video
    get_video(thread)


# Create the Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT"),
)
subreddits = ["AmItheAsshole", "offmychest"]

init()

for subreddit in subreddits:
    if not os.path.exists(f"assets/subreddits/{subreddit}"):
        os.mkdir(f"assets/subreddits/{subreddit}")

    subreddit = reddit.subreddit(subreddit)
    main()
