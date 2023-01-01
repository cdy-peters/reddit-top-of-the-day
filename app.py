"""Main"""

import os
import praw
from dotenv import load_dotenv

from thread import get_thread
from tts import get_audio

load_dotenv()


def init():
    """Initializes the program"""

    if not os.path.exists("assets"):
        os.mkdir("assets")
    if not os.path.exists("assets/temp"):
        os.mkdir("assets/temp")


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
get_audio(thread)
