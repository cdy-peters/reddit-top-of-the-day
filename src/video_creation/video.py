"""Creates the video"""

import time
import math
import json
import sys
import multiprocessing

from moviepy.editor import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips, CompositeAudioClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips

from src.utils.log_videos import log_videos, move_video
from src.video_creation.tts import TTS
from src.video_creation.screenshots import get_screenshots
from src.video_creation.background import get_subclip


def get_video(thread):
    """Gets the video"""

    # Get audio clips
    tts = TTS(thread["subreddit"], thread["id"])
    length = tts.get_audio(thread)
    if length is None:  # The the audio is too long
        return None

    # Add length to thread
    thread["length"] = length

    # Get screenshots
    get_screenshots(thread)

    # Get background
    get_subclip(thread["subreddit"], thread["id"], length)

    # Get video
    create_video(thread)

    # Add created_at to thread
    thread["created_at"] = math.floor(time.time())

    # Add thread object to thread.json
    path = f"assets/subreddits/{thread['subreddit']}/{thread['id']}"
    with open(f"{path}/thread.json", "w", encoding="utf-8") as f:
        json.dump(thread, f)

    # Add video to videos.json
    log_videos(thread["subreddit"], "pending_review", thread["id"])

    return thread


def create_video(thread):
    """Creates the video"""

    path = f"assets/subreddits/{thread['subreddit']}/{thread['id']}"

    # Get background clip
    background = VideoFileClip(f"{path}/background.mp4").without_audio()

    # Get audio clips
    audio = []
    audio.append(AudioFileClip(f"{path}/audio/title.mp3"))

    if thread["body"]:
        audio.append(AudioFileClip(f"{path}/audio/body.mp3"))

    for comment in thread["comments"]:
        audio.append(AudioFileClip(f"{path}/audio/{comment['id']}.mp3"))

    # Concat audio clips
    audio_concat = concatenate_audioclips(audio)
    audio_comp = CompositeAudioClip([audio_concat])

    # Get screenshots
    screenshots = []
    screenshots.append(
        ImageClip(f"{path}/screenshots/title.png")
        .set_duration(audio[0].duration)
        .resize(width=1030)
        .set_opacity(0.9)
        .crossfadein(0.2)
        .crossfadeout(0.2)
    )

    if thread["body"]:
        screenshots.append(
            ImageClip(f"{path}/screenshots/body.png")
            .set_duration(audio[1].duration)
            .resize(width=1030)
            .set_opacity(0.9)
            .crossfadein(0.2)
            .crossfadeout(0.2)
        )

    for i, comment in enumerate(thread["comments"]):
        if thread["body"]:
            i += 2
        else:
            i += 1

        screenshots.append(
            ImageClip(f"{path}/screenshots/{comment['id']}.png")
            .set_duration(audio[i].duration)
            .resize(width=1030)
            .set_opacity(0.9)
            .crossfadein(0.2)
            .crossfadeout(0.2)
        )

    # Concat screenshots
    screenshots_concat = concatenate_videoclips(screenshots).set_position("center")

    screenshots_concat.audio = audio_comp
    video = CompositeVideoClip([background, screenshots_concat])

    # Save video
    video.write_videofile(
        f"{path}/video.mp4",
        fps=30,
        audio_codec="aac",
        audio_bitrate="192k",
        threads=multiprocessing.cpu_count(),
    )


def remake_video(thread):
    """Remakes the video"""

    # Get audio clips
    tts = TTS(thread["subreddit"], thread["id"])
    length = tts.get_audio(thread)

    # Get background
    get_subclip(thread["subreddit"], thread["id"], length)

    # Get video
    create_video(thread)

    # Add created_at to thread
    thread["created_at"] = math.floor(time.time())

    # Add thread object to thread.json
    path = f"assets/subreddits/{thread['subreddit']}/{thread['id']}"
    with open(f"{path}/thread.json", "w", encoding="utf-8") as f:
        json.dump(thread, f)

    # Add video to videos.json
    move_video(thread["subreddit"], thread["id"], "pending_remake", "pending_review")


if __name__ == "__main__":
    THREAD = sys.argv[1]
    remake_video(json.loads(THREAD))
