"""Gets a thread and it's contents from a subreddit"""

import os
from praw.models import MoreComments


def check_threads(threads: list):
    """Check the threads for the highest score"""

    for thread in threads:
        # TODO: Check if the thread has been done
        # TODO: Check if the thread is NSFW
        # TODO: Check if the thread has comments
        return thread


def get_comments(thread):
    """Get the comments from the thread"""

    comments = []
    for comment in thread.comments:
        if isinstance(comment, MoreComments):
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

    threads = subreddit.top(time_filter="day", limit=1)
    thread = check_threads(threads)

    content = {}
    content["id"] = thread.id
    content["url"] = f"https://www.reddit.com{thread.permalink}"
    content["title"] = thread.title
    content["body"] = thread.selftext
    content["comments"] = get_comments(thread)

    os.mkdir(f"assets/threads/{content['id']}")

    return content
