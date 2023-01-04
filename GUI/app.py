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
    approved = data["approved"]

    if subreddit not in approved:
        approved[subreddit] = []
    approved[subreddit].append(thread)

    with open("../data/videos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # Move video to approved folder
    if not os.path.exists(f"../assets/approved/{subreddit}"):
        os.makedirs(f"../assets/approved/{subreddit}")

    os.rename(
        f"../assets/subreddits/{subreddit}/{thread}",
        f"../assets/approved/{subreddit}/{thread}",
    )
    if os.listdir(f"../assets/subreddits/{subreddit}") == []:
        os.rmdir(f"../assets/subreddits/{subreddit}")

    return redirect("/")


@app.route("/delete/<subreddit>/<thread>")
def delete(subreddit, thread):
    """Deletes video"""

    # Updates videos.json
    with open("../data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    deleted = data["deleted"]

    if subreddit not in deleted:
        deleted[subreddit] = []
    deleted[subreddit].append(thread)

    with open("../data/videos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # Delete video
    shutil.rmtree(f"../assets/subreddits/{subreddit}/{thread}")
    if os.listdir(f"../assets/subreddits/{subreddit}") == []:
        os.rmdir(f"../assets/subreddits/{subreddit}")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
