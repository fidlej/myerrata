
import re

def valid_int(value):
    """Converts the value to an integer value or zero.
    """
    try:
        result = int(value)
    except ValueError:
        result = 0

    return result


IGNORED_PREFIX_PATTERN = re.compile(ur"^(?:https?://)?(?:www\.)?")

def valid_url_prefix(value):
    """Returns a URL prefix without the http:// and "www." prefixes.
    """
    return IGNORED_PREFIX_PATTERN.sub(u"", value)

