"""Gets a thread and it's contents from a subreddit"""

import os
from datetime import datetime
from praw.models import MoreComments


def check_threads(threads: list):
    """Check the threads for the highest score"""

    for thread in threads:
        # TODO: Check if the thread has been done

        # Check if the thread is NSFW
        if thread.over_18:
            continue

        # Check if the thread has a sufficient amount of comments
        if thread.num_comments < 10:
            continue

        # Check if body is too long
        if len(thread.selftext) > 1500:
            continue

        # Check if created less than 24 hours ago
        now = datetime.utcnow()
        created = datetime.utcfromtimestamp(thread.created_utc)
        if (now - created).days > 1:
            continue

        return thread


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


def get_thread(subreddit):
    """Get a thread from the subreddit"""

    threads = subreddit.top(time_filter="day", limit=25)
    thread = check_threads(threads)

    # TODO: Handle if thread is None

    content = {}
    content["subreddit"] = thread.subreddit
    content["id"] = thread.id
    content["url"] = f"https://www.reddit.com{thread.permalink}"
    content["title"] = thread.title
    content["body"] = thread.selftext
    content["comments"] = get_comments(thread)

    os.mkdir(f"assets/subreddits/{content['subreddit']}/{content['id']}")

    return content
