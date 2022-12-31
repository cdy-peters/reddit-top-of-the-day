import praw
import os
from dotenv import load_dotenv
from thread import get_thread

load_dotenv()

# Create the Reddit instance
reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                     client_secret=os.getenv('CLIENT_SECRET'),
                     user_agent=os.getenv('USER_AGENT'))

# Get the subreddit
subreddit = reddit.subreddit('AmItheAsshole')

# Get the thread
thread = get_thread(subreddit)
print(thread)