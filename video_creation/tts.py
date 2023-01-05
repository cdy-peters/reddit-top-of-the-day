"""Gets the speech audio of the thread content"""

import os
import re
import shutil
import requests
from moviepy.editor import AudioFileClip, CompositeAudioClip, concatenate_audioclips


def check_text(text):
    """Checks and cleans the text"""

    # Remove links
    regex_urls = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
    text = re.sub(regex_urls, " ", text)

    # Remove special characters
    regex_expr = r"\s['|’]|['|’]\s|[\^_~@!;#:\-–—%“”‘\"%\*\/{}\[\]\(\)\\|<>=+]"
    text = re.sub(regex_expr, " ", text)

    # Replace symbols with words
    text = text.replace("+", "plus").replace("&", "and")

    # Trim whitespace
    text = re.sub(r"\s+", " ", text)

    # Expand acronyms
    text = re.sub(r"\bNTA\b", "Not The Asshole", text)
    text = re.sub(r"\bYTA\b", "You're The Asshole", text)
    text = re.sub(r"\bAITA\b", "Am I The Asshole", text)
    text = re.sub(r"\bETA\b", "Everyone's The Asshole", text)
    text = re.sub(r"\bNAH\b", "No Assholes Here", text)
    text = re.sub(r"\bTIFU\b", "Today I Fucked Up", text)

    if len(text) > 550:
        split_text = [
            i.group().strip() for i in re.finditer(r" *(((.|\n){0,550})(\.|.$))", text)
        ]
        return split_text

    return [text]


class TTS:
    """TTS class"""

    def __init__(self, subreddit, thread_id):
        self.subreddit = subreddit
        self.thread_id = thread_id
        self.length = 0

    def tts_handler(self, filename, text):
        """Handles the text to speech"""

        dir_path = f"assets/subreddits/{self.subreddit}/{self.thread_id}/audio"
        file_path = f"{dir_path}/{filename}"

        text = check_text(text)
        audio = []

        for i in text:
            url = "https://streamlabs.com/polly/speak"
            payload = {
                "voice": "Matthew",
                "text": i,
                "service": "polly",
            }

            try:
                response = requests.post(url, data=payload, timeout=10)  # ? Rate limit?
            except requests.exceptions.RequestException as err:
                print(err)
                return

            audio.append(response.json()["speak_url"])

        if len(audio) > 1:
            path = f"{dir_path}/temp"

            os.mkdir(path)

            for i, url in enumerate(audio):
                with open(f"{path}/{i}.mp3", "wb") as f:
                    f.write(requests.get(url, timeout=10).content)

            audio_clips = []
            for i in range(len(audio)):
                audio_clips.append(AudioFileClip(f"{path}/{i}.mp3"))

            CompositeAudioClip([concatenate_audioclips(audio_clips)]).write_audiofile(
                file_path, fps=44100
            )

            shutil.rmtree(path)
        else:
            with open(file_path, "wb") as f:
                f.write(requests.get(audio[0], timeout=10).content)

        self.length += AudioFileClip(file_path).duration

    def get_audio(self, thread):
        """Gets the audio of the thread"""

        os.mkdir(f"assets/subreddits/{self.subreddit}/{self.thread_id}/audio")

        # Title tts
        self.tts_handler("title.mp3", thread["title"])

        # Body tts
        if thread["body"]:
            self.tts_handler("body.mp3", thread["body"])

        if self.length > 60:  # Max length of video
            return None
        if self.length >= 45:
            thread["comments"] = []
            return self.length

        # Comments tts
        comments = []
        for comment in thread["comments"]:
            self.tts_handler(f'{comment["id"]}.mp3', comment["body"])

            if self.length >= 60:  # If new comment exceeds max length of video
                self.length -= AudioFileClip(
                    f'assets/subreddits/{self.subreddit}/{self.thread_id}/audio/{comment["id"]}.mp3'
                ).duration

                os.remove(
                    f'assets/subreddits/{self.subreddit}/{self.thread_id}/audio/{comment["id"]}.mp3'
                )

                thread["comments"] = comments
                break

            comments.append(comment)

        return self.length
