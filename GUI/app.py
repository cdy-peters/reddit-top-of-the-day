import os
import json
import shutil
import time
import math
from numerize import numerize
from flask import (
    Flask,
    render_template,
    send_from_directory,
    redirect,
    request,
    jsonify,
)

app = Flask(__name__)


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
                        "upvotes": numerize.numerize(thread_data["upvotes"]),
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

    return render_template("review.html", data=data)


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
    with open("../data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    pending_review = data["pending_review"]
    pending_upload = data["pending_upload"]

    if subreddit not in pending_upload:
        pending_upload[subreddit] = []
    pending_upload[subreddit].append(thread)

    pending_review[subreddit].remove(thread)
    if pending_review[subreddit] == []:
        pending_review.pop(subreddit)

    with open("../data/videos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return redirect("/")


@app.route("/queue_remake/<subreddit>/<thread>", methods=["GET", "POST"])
def queue_remake(subreddit, thread):
    """Queues video for remake"""

    if request.method == "POST":
        req_data = request.get_json()

        # Update thread.json
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

        with open(
            f"../assets/subreddits/{subreddit}/{thread}/thread.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(data, f, indent=4)

        # Update videos.json
        with open("../data/videos.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        pending_review = data["pending_review"]
        pending_remake = data["pending_remake"]

        if subreddit not in pending_remake:
            pending_remake[subreddit] = []
        pending_remake[subreddit].append(thread)

        pending_review[subreddit].remove(thread)
        if pending_review[subreddit] == []:
            pending_review.pop(subreddit)

        with open("../data/videos.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return jsonify({"success": True})

    return redirect("/")


@app.route("/delete/<subreddit>/<thread>")
def delete(subreddit, thread):
    """Deletes video"""

    # Updates videos.json
    with open("../data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    pending_review = data["pending_review"]
    deleted = data["deleted"]

    if subreddit not in deleted:
        deleted[subreddit] = []
    deleted[subreddit].append(thread)

    pending_review[subreddit].remove(thread)
    if pending_review[subreddit] == []:
        pending_review.pop(subreddit)

    with open("../data/videos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # Delete video
    subreddit_path = f"../assets/subreddits/{subreddit}"

    shutil.rmtree(f"{subreddit_path}/{thread}")
    if os.listdir(subreddit_path) == []:
        os.rmdir(subreddit_path)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
