
import logging
import wsgiref.handlers
from google.appengine.ext import webapp

from src import sane

DEBUG = True

class Handler(webapp.RequestHandler):
    def set_header(self, name, value):
        self.response.headers[name] = value

    def write(self, text):
        self.response.out.write(text)

    def write_json(self, array):
        from django.utils import simplejson
        self.write(simplejson.dumps(array))


class Save(Handler):
    def options(self):
        self._set_cors_headers()

    def _set_cors_headers(self):
        """Sets the needed CORS headers.
        """
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.set_header('Access-Control-Max-Age', str(20*24*3600))

    def post(self):
        """Saves a typo fix.
        The request is made by a Cross-Origin Resource Sharing (CORS) Ajax.

        GET parameters:
        url ... url of the fixed page.
        orig ... original text.
        new ... fixed text.
        pos ... 0 for an unique original text. It is the number
            of the same preceding texts on the page.
        """
        from src import diffing, writing
        # The incoming Content-Type is ignored.
        # XDomainRequest sends everything as text/plain.
        self.request.content_type = "application/x-www-form-urlencoded"
        self.request.environ.pop("webob._parsed_post_var", None)

        url = self.request.get("url")
        orig = self.request.get("orig")
        new = self.request.get("new")
        pos = sane.valid_int(self.request.get("pos"))
        page_order = sane.valid_int(self.request.get("page_order"))

        writing.save_fix(url, orig, new, pos, page_order)
        marked = diffing.mark_changes(orig, new)

        result = dict(marked='<span contenteditable="true">%s</span>' % marked);
        self._set_cors_headers()
        # We keep the text/html content-type. It is needed by iframes.
        self.write_json(result)


class Fixes(Handler):
    def get(self):
        from src import diffing, reading

        url = self.request.get("url")
        fixes = reading.find_fixes(url)
        results = []
        for fix in fixes:
            marked = diffing.mark_changes(fix.orig_text, fix.new_text)
            results.append(dict(
                orig=fix.orig_text,
                pos=fix.pos,
                marked=marked))

        self.write_json(dict(fixes=results))



class NotFound404(Handler):
    def get(self):
        logging.info('Wrong path: %s', self.request.path)
        self.error(404)
        self.write("No such page.")

    def post(self):
        self.get()


app = webapp.WSGIApplication(
        [
            ("/api/save", Save),
            ("/api/fixes", Fixes),
            ("/.*", NotFound404),
        ],
        debug=DEBUG)

def main():
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    from pylib import autoretry
    autoretry.autoretry_datastore_timeouts()
    main()

