from urllib.parse import urlparse


def check_is_link(string: str):
    return bool(urlparse(string).scheme)
