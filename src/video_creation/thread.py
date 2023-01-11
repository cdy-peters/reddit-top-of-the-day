"""Gets a thread and it's contents from a subreddit"""

import os
from datetime import datetime
from praw.models import MoreComments
from numerize import numerize

from utils.log_videos import video_exists
from utils.sanitize_text import clean_text


def get_comments(thread):
    """Get the comments from the thread"""

    comments = []
    for comment in thread.comments:
        if isinstance(comment, MoreComments):
            continue
        if comment.stickied:
            continue

        text = clean_text(comment.body)
        if len(text) <= 500 and len(text) > 50:
            comments.append(
                {
                    "id": comment.id,
                    "url": f"https://www.reddit.com{comment.permalink}",
                    "body": comment.body,
                }
            )
    return comments


def get_thread(thread, comments):
    """Performs checks on thread and gets the content of the thread"""

    # Check if the thread has been done
    if video_exists(thread.subreddit.display_name, thread.id):
        return None

    # Check if the thread has a sufficient amount of comments
    if thread.num_comments < 10:
        return None

    # Check if body is too long
    if len(thread.selftext) > 1500:
        return None

    # Check if created less than 24 hours ago
    now = datetime.utcnow()
    created = datetime.utcfromtimestamp(thread.created_utc)
    if (now - created).days > 1:
        return None

    # Get comments
    if comments:
        comments = get_comments(thread)
    else:
        comments = []

    content = {
        "subreddit": thread.subreddit.display_name,
        "id": thread.id,
        "url": f"https://www.reddit.com{thread.permalink}",
        "over_18": thread.over_18,
        "upvotes": numerize.numerize(thread.ups),
        "author": thread.author.name,
        "title": thread.title,
        "body": thread.selftext,
        "comments": comments,
    }

    os.mkdir(f"assets/subreddits/{content['subreddit']}/{content['id']}")

    return content
