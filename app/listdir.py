"""
A simple filesystem browser.
It allows to see the deployed files on appengine.
Enable it in your app.yml:
    - url: /listdir.*
      script: listdir.py
      login: admin


Author: Ivo Danihelka <ivo@danihelka.net>
License: MIT
"""

import os
import urllib
from cgi import escape

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

LISTDIR_URL = "/listdir"
ROOT_DIR = "."
DEBUG = True

class FileServer(webapp.RequestHandler):
    def get(self, path):
        path = path.strip("/")
        if os.path.isdir(_onfs(path)):
            output = _render_dir(path)
        else:
            self.response.headers["Content-Type"] = "text/plain"
            output = _render_file(path)

        self.response.out.write(output)


def _onfs(path):
    return "%s/%s" % (ROOT_DIR, path)

def _render_dir(path):
    filenames = os.listdir(_onfs(path))
    filenames.sort()
    output = "<html><head><title>%s</title><body>\n" % escape(path)
    output += "<b>%s</b>" % _link_to_components(path)
    output += "<hr/><ul>\n"
    prefix = path
    if prefix:
        prefix += "/"

    for name in filenames:
        displayname = name
        child_path = prefix + name
        if os.path.isdir(_onfs(child_path)):
            displayname += "/"

        output += '<li>%s</li>\n' % _link_to(child_path, displayname)

    output += "</ul><hr/></body></html>"
    return output

def _link_to_components(path):
    output = _link_to("", os.path.realpath(ROOT_DIR))
    output += " / "
    if not path:
        return output

    prefix = ""
    for part in path.split("/"):
        child_path = prefix + part
        output += _link_to(child_path, part)
        output += " / "
        prefix = child_path + "/"

    return output

def _link_to(path, name):
    return '<a href="%s">%s</a>' % (
        urllib.quote(LISTDIR_URL + "/" + path), escape(name))

def _render_file(path):
    return open(_onfs(path), "rb").read()


def main():
    app = webapp.WSGIApplication(
            [
                (LISTDIR_URL + "(.*)", FileServer),
            ],
            debug=DEBUG)
    run_wsgi_app(app)

if __name__ == "__main__":
    main()

