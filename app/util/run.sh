#!/bin/sh
exec ../../google_appengine/dev_appserver.py --port 9999 "$@" .
