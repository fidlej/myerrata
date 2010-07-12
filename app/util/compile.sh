#!/bin/sh
set -e
for name in myerrata bookmarklet ; do
    echo "Compiling $name" >&2
    java -jar ../../closure-compiler/compiler.jar --js "static/js/$name.js" --js_output_file "static/js/$name.min.js" --warning_level VERBOSE "$@"
done
