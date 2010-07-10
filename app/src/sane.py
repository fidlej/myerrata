
import re

class BadRequestError(ValueError):
    pass


def valid_int(value):
    """Converts the value to an integer value or zero.
    """
    try:
        result = int(value)
    except ValueError:
        result = 0

    return result


URL_PATTERN = re.compile(r"^https?://([^#]+)")

def valid_url(url):
    match = URL_PATTERN.match(url)
    if match is None:
        #TODO: raise a HTTP error
        raise BadRequestError("Invalid HTTP URL: %r" % url)

    url = match.group(1)
    if len(url) > 500:
        raise BadRequestError("Too long URL: %r" % url)

    return url

