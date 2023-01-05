import json


def log_videos(subreddit, key, thread_id):
    """Log thread ID to videos.json"""

    with open("data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if subreddit not in data[key]:
        data[key][subreddit] = []

    data[key][subreddit].append(thread_id)

    with open("data/videos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def video_exists(subreddit, thread_id):
    """Check if thread ID is in videos.json"""

    with open("data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for key in data:
        if subreddit in data[key]:
            if thread_id in data[key][subreddit]:
                return True

    return False
