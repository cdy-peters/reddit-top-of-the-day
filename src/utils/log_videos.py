import json
import os


def log_videos(subreddit, key, thread_id):
    """Log thread ID to videos.json"""

    with open("data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if subreddit not in data[key]:
        data[key][subreddit] = []

    if thread_id not in data[key][subreddit]:
        data[key][subreddit].append(thread_id)

    with open("data/videos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def move_video(subreddit, thread, current, new):
    """Move video to new thread"""

    src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = f"{src_path}/data/videos.json"

    # Update videos.json
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pending_current = data[current]
    pending_new = data[new]

    if subreddit not in pending_new:
        pending_new[subreddit] = []
    pending_new[subreddit].append(thread)

    pending_current[subreddit].remove(thread)
    if pending_current[subreddit] == []:
        pending_current.pop(subreddit)

    with open(path, "w", encoding="utf-8") as f:
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
