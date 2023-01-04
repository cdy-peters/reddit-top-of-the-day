"""Gets a thread and it's contents from a subreddit"""

import os
import json
from datetime import datetime
from praw.models import MoreComments


def get_comments(thread):
    """Get the comments from the thread"""

    comments = []
    for comment in thread.comments:
        if isinstance(comment, MoreComments):
            continue
        if comment.stickied:
            continue
        if len(comment.body) <= 500:
            comments.append(
                {
                    "id": comment.id,
                    "url": f"https://www.reddit.com{comment.permalink}",
                    "body": comment.body,
                }
            )
    return comments


def get_thread(thread):
    """Gets the content of the thread"""

    # Check if the thread has been done
    with open("data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if thread.subreddit.display_name in data["pending"]:
        if thread.id in data["pending"][thread.subreddit.display_name]:
            return None
    if thread.subreddit.display_name in data["approved"]:
        if thread.id in data["approved"][thread.subreddit.display_name]:
            return None
    if thread.subreddit.display_name in data["deleted"]:
        if thread.id in data["deleted"][thread.subreddit.display_name]:
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

    content = {
        "subreddit": thread.subreddit.display_name,
        "id": thread.id,
        "url": f"https://www.reddit.com{thread.permalink}",
        "over_18": thread.over_18,
        "title": thread.title,
        "body": thread.selftext,
        "comments": get_comments(thread),
    }

    os.mkdir(f"assets/subreddits/{content['subreddit']}/{content['id']}")

    return content
