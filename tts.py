import requests


def get_speech(text, path):
    # TODO: Check if the text is too long
    # TODO: Check if the text is empty
    # TODO: Clean text, removing links, special characters, extending abbreviations

    url = "https://streamlabs.com/polly/speak"
    max_chars = 550
    payload = {
        "voice": "Matthew",
        "text": text,
        "service": "polly",
    }
    response = requests.post(url, data=payload)
    speech = response.json()['speak_url']
    with open(path, 'wb') as f:
        f.write(requests.get(speech).content)
