import os
import json
import shutil
from flask import Flask, render_template, send_from_directory, redirect, request

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


@app.route("/edit/body/<subreddit>/<thread>", methods=["GET", "POST"])
def edit_body(subreddit, thread):
    """Edits body of video"""

    if request.method == "POST":
        with open(
            f"../assets/subreddits/{subreddit}/{thread}/thread.json",
            "r",
            encoding="utf-8",
        ) as f:
            data = json.load(f)

        data["body"] = request.form["body"]

        with open(
            f"../assets/subreddits/{subreddit}/{thread}/thread.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(data, f, indent=4)

        return "Success"

    return redirect("/")


@app.route("/edit/comment/<subreddit>/<thread>/<comment_id>", methods=["GET", "POST"])
def edit_comment(subreddit, thread, comment_id):
    """Edits comment of video"""

    if request.method == "POST":
        with open(
            f"../assets/subreddits/{subreddit}/{thread}/thread.json",
            "r",
            encoding="utf-8",
        ) as f:
            data = json.load(f)

        comments = data["comments"]
        for i, comment in enumerate(comments):
            if comment["id"] == comment_id:
                comments[i]["body"] = request.form["comment"]
                break

        with open(
            f"../assets/subreddits/{subreddit}/{thread}/thread.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(data, f, indent=4)

        return "Success"

    return redirect("/")


@app.route("/queue_upload/<subreddit>/<thread>")
def queue_upload(subreddit, thread):
    """Approves video"""

    # Update videos.json
    with open("../data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    pending_review = data["pending_review"]
    approved_upload = data["pending_upload"]

    if subreddit not in approved_upload:
        approved_upload[subreddit] = []
    approved_upload[subreddit].append(thread)

    pending_review[subreddit].remove(thread)
    if pending_review[subreddit] == []:
        pending_review.pop(subreddit)

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


@app.route("/queue_remake/<subreddit>/<thread>")
def queue_remake(subreddit, thread):
    """Queues video for remake"""

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
