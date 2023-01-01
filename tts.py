"""Gets the speech audio of the thread content"""

import os
import re
import requests


def check_text(text):
    """Checks and cleans the text"""

    # TODO: Clean text, removing links, special characters, extending abbreviations

    if len(text) > 1000:
        split_text = [
            i.group().strip()
            for i in re.finditer(
                r" *(((.|\n){0,550})(\.|.$))", text
            )
        ]
        return split_text

    return [text]


def tts_handler(text, path):
    """Handles the text to speech"""

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
            response = requests.post(
                url, data=payload, timeout=10)  # ? Rate limit?
        except requests.exceptions.RequestException as err:
            print(err)
            return

        audio.append(response.json()['speak_url'])

    if len(audio) > 1:
        # TODO: Merge audio clips
        print(len(audio))
    else:
        with open(path, 'wb') as f:
            f.write(requests.get(audio[0], timeout=10).content)

    # TODO: Check if total length of speech is too long


def get_audio(thread):
    """Gets the audio of the thread"""

    os.mkdir(f'assets/{thread["id"]}')

    tts_handler(thread['title'], f'assets/{thread["id"]}/title.mp3')
    tts_handler(thread['body'], f'assets/{thread["id"]}/body.mp3')
    for comment in thread['comments']:
        tts_handler(comment['body'],
                    f'assets/{thread["id"]}/{comment["id"]}.mp3')