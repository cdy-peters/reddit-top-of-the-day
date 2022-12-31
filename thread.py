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
                    "url": comment.permalink,
                    "body": comment.body,
                }
            )
    return comments

def get_thread(subreddit):
    threads = subreddit.top(time_filter='day', limit=1)
    thread = check_threads(threads)

    thread_obj = {}
    thread_obj["id"] = thread.id
    thread_obj["url"] = f"https://www.reddit.com{thread.permalink}"
    thread_obj["title"] = thread.title
    thread_obj["post"] = thread.selftext
    thread_obj['comments'] = get_comments(thread)

    return thread_obj