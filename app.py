"""Main"""

import os
import praw
from dotenv import load_dotenv

from thread import get_thread
from tts import get_audio
from screenshots import get_screenshots
from background import get_subclip

load_dotenv()


def init():
    """Initializes the program"""

    if not os.path.exists("assets"):
        os.mkdir("assets")

    if not os.path.exists("assets/threads"):
        os.mkdir("assets/threads")

    if not os.path.exists("assets/backgrounds"):
        os.mkdir("assets/backgrounds")


init()

# Create the Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT"),
)

# Get the subreddit
subreddit = reddit.subreddit("AmItheAsshole")

# Get the thread
thread = get_thread(subreddit)

# Get audio clips
length = get_audio(thread)

# Get screenshots
get_screenshots(thread)

# Get background
get_subclip(thread["id"], length)
