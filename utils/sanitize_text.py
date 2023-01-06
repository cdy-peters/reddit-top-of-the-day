import re


def clean_text(text):
    """Removes unnecessary parts of text"""

    # Remove links
    regex_urls = r"^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    text = re.sub(regex_urls, " ", text)

    # Remove special characters
    regex_expr = r"\s['|’]|['|’]\s|[\^_~@!;#:\-–—%“”‘\"%\*\/{}\[\]\(\)\\|<>=+]"
    text = re.sub(regex_expr, " ", text)

    # Replace symbols with words
    text = text.replace("+", "plus").replace("&", "and")

    # Trim whitespace
    text = re.sub(r"\s+", " ", text)

    return text


def expand_acronyms(text):
    """Expands acronyms"""

    text = re.sub(r"\bNTA\b", "Not The Asshole", text)
    text = re.sub(r"\bYTA\b", "You're The Asshole", text)
    text = re.sub(r"\bAITA\b", "Am I The Asshole", text)
    text = re.sub(r"\bWIBTA\b", "Would I be the Asshole", text)
    text = re.sub(r"\bETA\b", "Everyone's The Asshole", text)
    text = re.sub(r"\bNAH\b", "No Assholes Here", text)
    text = re.sub(r"\bTIFU\b", "Today I Fucked Up", text)

    return text


def check_text(text):
    """Checks and cleans the text"""

    text = clean_text(text)

    text = expand_acronyms(text)

    if len(text) > 550:
        split_text = [
            i.group().strip() for i in re.finditer(r" *(((.|\n){0,550})(\.|.$))", text)
        ]
        return split_text

    return [text]
