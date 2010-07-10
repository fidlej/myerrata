
from nose.tools import eq_

from src import sane

def test_valid_url():
    f = sane.valid_url
    eq_(f("http://localhost:9999/"), "localhost:9999/")
    eq_(f("http://example.com/path/to?something=hello#here"),
            "example.com/path/to?something=hello")
    eq_(f("https://example.com/path/"),
            "example.com/path/")

    _bad_url("")
    _bad_url("javascript:alert('hello')")
    _bad_url("something else")


def _bad_url(url):
    try:
        sane.valid_url(url)
        assert False
    except sane.BadRequestError:
        pass
