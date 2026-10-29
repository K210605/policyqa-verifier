import re


def tokenize(text):
    text = text.lower()
    return re.findall(r"[a-z0-9]+(?:[.\-][a-z0-9]+)*", text)