
from nose.tools import eq_

from src import model

def test_normalize_url():
    eq_(model.normalize_url("http://localhost:9999/"), "localhost:9999/")
    eq_(model.normalize_url("http://example.com/path/to?something=hello#here"),
            "example.com/path/to?something=hello")
    eq_(model.normalize_url("https://example.com/path/"),
            "example.com/path/")

