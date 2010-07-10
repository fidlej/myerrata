
import re

URL_PREFIX_PATTERN = re.compile(
        ur"^(?:https?://)?(?:www\.)?([^:/]*)(?::\d+)?([^?#]*)([^#]*)")

def normalize_query(query):
    """Normalizes the URL for a search index.
    Strips http://, "www.", the port number and a trailing / from the URL.
    """
    match = URL_PREFIX_PATTERN.match(query.strip().lower())
    domain, path, query = match.groups(u'')
    path = path.rstrip('/')
    return "".join((domain, path, query))


def strip_www(url):
    return normalize_query(url)

