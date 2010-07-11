
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import fix_path
from src import config, sane


class Handler(webapp.RequestHandler):
    def set_header(self, name, value):
        self.response.headers[name] = value

    def write(self, text):
        self.response.out.write(text)

    def write_json(self, array, jsonp_callback=u""):
        from django.utils import simplejson
        json = simplejson.dumps(array)
        if jsonp_callback:
            result = u"%s(%s)" % (jsonp_callback, json)
        else:
            result = json

        self.write(result)

    def render(self, template, **kw):
        from src import templating, formatting
        kw["formatting"] = formatting
        self.write(templating.render(template, **kw))

    def handle_exception(self, e, debug_mode):
        if isinstance(e, sane.BadRequestError):
            logging.info('Wrong path: %r', self.request.path)
            self.error(400)
            self.write(str(e))
            return

        return webapp.RequestHandler.handle_exception(self, e, debug_mode)


class SaveHandler(Handler):
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
        from src import writing
        # The incoming Content-Type is ignored.
        # XDomainRequest sends everything as text/plain.
        self.request.content_type = "application/x-www-form-urlencoded"
        self.request.environ.pop("webob._parsed_post_var", None)

        url = sane.valid_url(self.request.get("url"))
        orig = self.request.get("orig")
        new = self.request.get("new")
        pos = sane.valid_int(self.request.get("pos"))
        page_order = sane.valid_int(self.request.get("page_order"))

        fix = writing.save_fix(url, orig, new, pos, page_order)
        marked = fix.mark_changes()

        result = dict(marked=marked);
        self._set_cors_headers()
        # We keep the text/html content-type. It is needed by iframes.
        self.write_json(result)


class FixesHandler(Handler):
    def get(self):
        from src import reading

        url = sane.valid_url(self.request.get("url"))
        callback = self.request.get("callback")
        fixes = reading.find_fixes(url)
        results = []
        for fix in fixes:
            marked = fix.mark_changes()
            results.append(dict(
                orig=fix.orig_text,
                pos=fix.pos,
                gone=fix.gone,
                marked=marked))

        self.write_json(dict(fixes=results), jsonp_callback=callback)


class SearchHandler(Handler):
    def get(self):
        from src import reading, visual

        q = self.request.get("q")
        limit = 100
        fixes = reading.search(q, limit)
        if len(fixes) != limit:
            limit = None 
        url_fixes = visual.group_by_url(fixes)

        title = u"%s fixes" % q
        self.render("search.html", title=title, url_fixes=url_fixes, q=q,
                limit=limit)


class NotFound404Handler(Handler):
    def get(self):
        logging.info('Wrong path: %s', self.request.path)
        self.error(404)
        self.write("No such page.")

    def post(self):
        self.get()


app = webapp.WSGIApplication(
        [
            ("/api/save", SaveHandler),
            ("/api/fixes", FixesHandler),
            ("/search", SearchHandler),
            ("/.*", NotFound404Handler),
        ],
        debug=config.DEBUG)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    import autoretry
    autoretry.autoretry_datastore_timeouts()
    main()

