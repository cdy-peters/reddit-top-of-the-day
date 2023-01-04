import os
import json
import shutil
from flask import Flask, render_template, send_from_directory, redirect

app = Flask(__name__)


@app.route("/")
def index():
    """Retrieves data of created videos and returns them to page"""

    videos = {}

    subreddits = os.listdir("../assets/subreddits")

    for subreddit in subreddits:
        threads = os.listdir(f"../assets/subreddits/{subreddit}")

        thread_videos = {}
        for thread in threads:
            if not os.path.exists(
                f"../assets/subreddits/{subreddit}/{thread}/thread.json"
            ):
                continue

            with open(
                f"../assets/subreddits/{subreddit}/{thread}/thread.json",
                "r",
                encoding="utf-8",
            ) as f:
                data = json.load(f)
                thread_videos[thread] = data

        videos[subreddit] = thread_videos

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


@app.route("/approve/<subreddit>/<thread>")
def approve(subreddit, thread):
    """Approves video"""

    # Update videos.json
    with open("../data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    pending = data["pending"]
    approved = data["approved"]

    if subreddit not in approved:
        approved[subreddit] = []
    approved[subreddit].append(thread)

    pending[subreddit].remove(thread)
    if pending[subreddit] == []:
        pending.pop(subreddit)

    with open("../data/videos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # Move video to approved folder, deleting unnecessary files
    subreddit_path = f"../assets/subreddits/{subreddit}"

    shutil.rmtree(f"{subreddit_path}/{thread}/audio")
    shutil.rmtree(f"{subreddit_path}/{thread}/screenshots")
    os.remove(f"{subreddit_path}/{thread}/background.mp4")

    if not os.path.exists(f"../assets/approved/{subreddit}"):
        os.makedirs(f"../assets/approved/{subreddit}")

    os.rename(
        f"{subreddit_path}/{thread}",
        f"../assets/approved/{subreddit}/{thread}",
    )
    if os.listdir(subreddit_path) == []:
        os.rmdir(subreddit_path)

    return redirect("/")


@app.route("/delete/<subreddit>/<thread>")
def delete(subreddit, thread):
    """Deletes video"""

    # Updates videos.json
    with open("../data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    pending = data["pending"]
    deleted = data["deleted"]

    if subreddit not in deleted:
        deleted[subreddit] = []
    deleted[subreddit].append(thread)

    pending[subreddit].remove(thread)
    if pending[subreddit] == []:
        pending.pop(subreddit)

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
