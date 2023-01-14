import os
import json
import shutil
import time
import math
import subprocess

from multiprocessing.pool import ThreadPool
from flask import (
    Flask,
    render_template,
    send_from_directory,
    redirect,
    request,
    jsonify,
)

from src.utils.log_videos import move_video

app = Flask(__name__)

pool = ThreadPool(processes=1)


def get_created_since(created_at):
    """Returns how long ago the video was created"""

    seconds = math.floor(time.time()) - created_at
    minutes = math.floor(seconds / 60)
    hours = math.floor(minutes / 60)
    days = math.floor(hours / 24)
    weeks = math.floor(days / 7)
    months = math.floor(days / 30)
    years = math.floor(days / 365)

    if seconds < 60:
        val = seconds
        unit = "second"
    elif minutes < 60:
        val = minutes
        unit = "minute"
    elif hours < 24:
        val = hours
        unit = "hour"
    elif days < 7:
        val = days
        unit = "day"
    elif weeks < 4:
        val = weeks
        unit = "week"
    elif months < 12:
        val = months
        unit = "month"
    else:
        val = years
        unit = "year"

    if val == 1:
        return f"Created {val} {unit} ago"
    return f"Created {val} {unit}s ago"


@app.route("/")
def index():
    """Retrieves data of created videos and returns them to page"""

    video_types = ["pending_review", "pending_remake", "pending_upload"]
    videos = {}

    with open("../data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for video_type in video_types:
        for subreddit in data[video_type]:
            if subreddit not in videos:
                videos[subreddit] = []

            for thread in data[video_type][subreddit]:
                with open(
                    f"../assets/subreddits/{subreddit}/{thread}/thread.json",
                    "r",
                    encoding="utf-8",
                ) as f:
                    thread_data = json.load(f)

                videos[subreddit].append(
                    {
                        "type": video_type,
                        "id": thread_data["id"],
                        "title": thread_data["title"],
                        "over_18": thread_data["over_18"],
                        "upvotes": thread_data["upvotes"],
                        "length": thread_data["length"],
                        "created_since": get_created_since(thread_data["created_at"]),
                    }
                )

    return render_template("index.html", videos=videos)


@app.route("/review/<subreddit>/<thread>")
def review(subreddit, thread):
    """Returns review page"""

    with open(
        f"../assets/subreddits/{subreddit}/{thread}/thread.json", "r", encoding="utf-8"
    ) as f:
        data = json.load(f)

    data["created_since"] = get_created_since(data["created_at"])

    return render_template("review.html", thread=data)


@app.route("/video/<subreddit>/<thread>")
def video(subreddit, thread):
    """Returns video"""

    return send_from_directory(
        f"../assets/subreddits/{subreddit}/{thread}", "video.mp4"
    )


@app.route("/queue_upload/<subreddit>/<thread>")
def queue_upload(subreddit, thread):
    """Approves video for upload"""

    # Update videos.json
    move_video(subreddit, thread, "pending_review", "pending_upload")

    return redirect("/")


@app.route("/queue_remake/<subreddit>/<thread>", methods=["GET", "POST"])
def queue_remake(subreddit, thread):
    """Queues video for remake"""

    if request.method == "POST":
        req_data = request.get_json()

        # Get thread.json
        with open(
            f"../assets/subreddits/{subreddit}/{thread}/thread.json",
            "r",
            encoding="utf-8",
        ) as f:
            data = json.load(f)

        # Replace body
        if "body" in req_data:
            data["body"] = req_data["body"]

        # Replace comments
        if req_data["comments"]:
            for comment in req_data["comments"]:
                for old_comment in data["comments"]:
                    if old_comment["id"] == comment:
                        old_comment["body"] = req_data["comments"][comment]

        # Save thread.json
        with open(
            f"../assets/subreddits/{subreddit}/{thread}/thread.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(data, f, indent=4)

        # Remove audio files
        shutil.rmtree(f"../assets/subreddits/{subreddit}/{thread}/audio")

        # Update videos.json
        move_video(subreddit, thread, "pending_review", "pending_remake")

        # Queue remake as a subprocess
        pool.apply_async(
            subprocess.Popen(
                ["python", "video_creation/remake_video.py", json.dumps(data)],
                cwd="../../src/",
            )
        )

        return jsonify({"success": True})

    return redirect("/")


@app.route("/delete/<subreddit>/<thread>")
def delete(subreddit, thread):
    """Deletes video"""

    # Updates videos.json
    move_video(subreddit, thread, "pending_review", "deleted")

    # Delete video
    subreddit_path = f"../assets/subreddits/{subreddit}"

    shutil.rmtree(f"{subreddit_path}/{thread}")
    if os.listdir(subreddit_path) == []:
        os.rmdir(subreddit_path)

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
