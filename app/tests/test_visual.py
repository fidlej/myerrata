
from nose.tools import eq_

from src import visual

def test_group_by_url():
    url_fixes = visual.group_by_url(
        fake_fixes("hello", "hello", "how are you"))

    eq_(len(url_fixes), 2)
    url, fixes = url_fixes[0]
    eq_(fixes[0].url, "hello")
    eq_(fixes[1].url, "hello")
    eq_(fixes[1].page_order, 1)


def fake_fixes(*urls):
    class Mock:
        pass

    fixes = []
    for i, url in enumerate(urls):
        fix = Mock()
        fix.url = url
        fix.page_order = i
        fixes.append(fix)

    return fixes

