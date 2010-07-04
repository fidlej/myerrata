
from nose.tools import eq_

from src import sane

def test_valid_url_prefix():
    eq_(sane.valid_url_prefix(""), "")
    eq_(sane.valid_url_prefix("http://localhost:9999/"), "localhost:9999/")
    eq_(sane.valid_url_prefix("www.google.com"), "google.com")
    eq_(sane.valid_url_prefix("https://google.com"), "google.com")
    eq_(sane.valid_url_prefix("http://www.google.com"), "google.com")
    eq_(sane.valid_url_prefix("www.google.com/search?q=me&lang=en#here"),
            "google.com/search?q=me&lang=en")

