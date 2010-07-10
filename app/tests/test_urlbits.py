
from nose.tools import eq_

from src import urlbits

def test_normalize_query():
    f = urlbits.normalize_query
    eq_(f(""), "")
    eq_(f("http://localHost:9999/"), "localhost")
    eq_(f("  www.google.com"), "google.com")
    eq_(f("https://google.com"), "google.com")
    eq_(f("http://www.google.com"), "google.com")
    eq_(f("www.google.com/search?q=me&lang=en#here"),
            "google.com/search?q=me&lang=en")
    eq_(f("example.com/my/?q=param"), "example.com/my?q=param")
