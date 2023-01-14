"""Gets the speech audio of the thread content"""

import os
import shutil

from moviepy.editor import AudioFileClip, CompositeAudioClip, concatenate_audioclips

from src.utils.sanitize_text import check_text, split_text
from src.utils.voices import streamlabs


class TTS:
    """TTS class"""

    def __init__(self, subreddit, thread_id):
        self.subreddit = subreddit
        self.thread_id = thread_id
        self.path = os.path.abspath(
            f"assets/subreddits/{self.subreddit}/{self.thread_id}"
        )
        self.length = 0
        self.last_clip_length = 0

    def tts_handler(self, filename, text):
        """Handles the text to speech"""

        dir_path = f"{self.path}/audio"
        file_path = f"{dir_path}/{filename}"

        text = check_text(text)

        if len(text) <= 550:
            streamlabs(text, file_path)
        else:
            path = f"{dir_path}/temp"
            os.mkdir(path)

            text = split_text(text)
            audio = []
            for i, t in enumerate(text):
                streamlabs(t, f"{path}/{i}.mp3")
                audio.append(AudioFileClip(f"{path}/{i}.mp3"))

            CompositeAudioClip([concatenate_audioclips(audio)]).write_audiofile(
                file_path, fps=44100
            )

            shutil.rmtree(path)

        # Add length of clip to total length
        clip = AudioFileClip(file_path)
        clip.close()
        self.length += clip.duration
        self.last_clip_length = clip.duration

    def get_audio(self, thread):
        """Gets the audio of the thread"""

        os.mkdir(f"{self.path}/audio")

        # Title tts
        self.tts_handler("title.mp3", thread["title"])

        # Body tts
        if thread["body"]:
            self.tts_handler("body.mp3", thread["body"])

        if self.length > 60:  # Max length of video
            # Delete thread directory
            shutil.rmtree(f"{self.path}")
            return None
        if self.length >= 45:
            thread["comments"] = []
            return self.length

        # Comments tts
        comments = []
        for comment in thread["comments"]:
            self.tts_handler(f'{comment["id"]}.mp3', comment["body"])

            if self.length >= 60:  # If new comment exceeds max length of video
                # Delete last clip
                path = f'{self.path}/audio/{comment["id"]}.mp3'
                os.remove(path)

                # Remove length of last clip from total length
                self.length -= self.last_clip_length

                thread["comments"] = comments
                break

            comments.append(comment)

        return self.length
