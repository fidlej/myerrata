
import re

URL_PREFIX_PATTERN = re.compile(
        ur"^(?:https?://)?(?:www\.)?([^:/]*)(?::\d+)?([^?#]*)([^#]*)")

def strip_www(url):
    """Normalizes the URL for a search index.
    Strips http://, "www.", the port number and a trailing / from the URL.
    """
    match = URL_PREFIX_PATTERN.match(url.strip().lower())
    host, path, query = match.groups(u'')
    path = path.rstrip('/')
    return "".join((host, path, query))

