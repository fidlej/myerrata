
from nose.tools import eq_

from src import urlbits

def test_strip_www():
    f = urlbits.strip_www
    eq_(f(""), "")
    eq_(f("http://localHost:9999/"), "localhost")
    eq_(f("  www.google.com"), "google.com")
    eq_(f("https://google.com"), "google.com")
    eq_(f("http://www.google.com"), "google.com")
    eq_(f("www.google.com/search?q=me&lang=en#here"),
            "google.com/search?q=me&lang=en")
    eq_(f("example.com/my/?q=param"), "example.com/my?q=param")
    eq_(f("ww"), "ww")
    eq_(f("htt"), "htt")
