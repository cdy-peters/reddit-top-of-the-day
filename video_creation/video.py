"""Creates the video"""

import multiprocessing

from moviepy.editor import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips, CompositeAudioClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips


def get_video(thread):
    """Creates the video"""

    path = f"assets/subreddits/{thread['subreddit']}/{thread['id']}"

    # Get background clip
    background = VideoFileClip(f"{path}/background.mp4").without_audio()

    # Get audio clips
    audio = []
    audio.append(AudioFileClip(f"{path}/audio/title.mp3"))
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
        .resize(width=980)
        .set_opacity(0.9)
        .crossfadein(0.2)
        .crossfadeout(0.2)
    )
    screenshots.append(
        ImageClip(f"{path}/screenshots/body.png")
        .set_duration(audio[1].duration)
        .resize(width=980)
        .set_opacity(0.9)
        .crossfadein(0.2)
        .crossfadeout(0.2)
    )
    for i, comment in enumerate(thread["comments"]):
        screenshots.append(
            ImageClip(f"{path}/screenshots/{comment['id']}.png")
            .set_duration(audio[i + 2].duration)
            .resize(width=980)
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
