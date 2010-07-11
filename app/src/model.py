
import time
import re
from google.appengine.ext import db

class Fix(db.Model):
    """A fix for a typo.
    """
    url = db.StringProperty(required=True)
    stripped_url = db.StringProperty(required=True)
    orig_text = db.TextProperty(required=True)
    new_text = db.TextProperty()
    # The pos tells the position of equal orig texts on a page.
    pos = db.IntegerProperty(required=True, indexed=False)
    # The page_order defines visual ordering of fixes on a page.
    page_order = db.IntegerProperty(required=True)
    updated_at = db.IntegerProperty(required=True)
    # A fix is marked as gone if the orig_text is no longer on the page.
    gone = db.BooleanProperty(required=True, default=False)

    @classmethod
    def prepare(cls, url, orig_text, new_text, pos, page_order):
        """Prepares all required properties before
        calling the constructor.
        """
        from src import urlbits
        stripped_url = urlbits.strip_www(url)
        key_name = _compute_key_name(url, pos, orig_text)
        updated_at = int(time.time())
        return Fix(key_name=key_name,
                url=url, stripped_url=stripped_url,
                orig_text=orig_text, new_text=new_text,
                pos=pos, page_order=page_order, updated_at=updated_at)

    @property
    def key_name(self):
        return self.key().name()

    def mark_changes(self):
        from src import diffing
        return diffing.mark_changes(self.orig_text, self.new_text)


def _compute_key_name(url, pos, orig_text):
    import base64
    import hashlib
    domain = url.split('/', 1)[0][:400]

    m = hashlib.sha1()
    m.update(url.encode("utf-8"))
    m.update('#')
    m.update(str(pos))
    m.update('#')
    m.update(orig_text.encode("utf-8"))
    return domain + "#" + base64.urlsafe_b64encode(m.digest())

