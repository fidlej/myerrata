#!/bin/sh
# Python2.6 is used to have SSL
exec `which python2.6 python | head -1` ../../google_appengine/appcfg.py "$@" update .
