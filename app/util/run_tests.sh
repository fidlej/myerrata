#!/bin/sh
PYTHONPATH=../../google_appengine:../../google_appengine/lib/yaml/lib exec nosetests "$@"
