"""Voices for TTS"""

import time
import requests

def streamlabs(text, file_path):
    """Streamlabs TTS"""

    url = "https://streamlabs.com/polly/speak"
    payload = {
        "voice": "Matthew",
        "text": text,
        "service": "polly",
    }
    response = requests.post(url, data=payload, timeout=10)

    while response.status_code == 429:
        time.sleep(int(response.headers["retry-after"]))
        response = requests.post(url, data=payload, timeout=10)

    audio = requests.get(response.json()["speak_url"], timeout=10)

    with open(file_path, "wb") as f:
        f.write(audio.content)