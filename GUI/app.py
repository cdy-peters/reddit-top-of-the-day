import os
import json
from flask import Flask, render_template, send_from_directory

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


if __name__ == "__main__":
    app.run(debug=True)
