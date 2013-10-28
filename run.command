#!/usr/bin/env sh

echo $0
SCRIPT_PATH=$(DIR=`dirname "$0"` ; cd "$DIR" ; echo "$PWD")
echo $SCRIPT_PATH
STARTUP_CMD="from pypl import *
print 'To run only the fast examples, type \"execfile(\'Examples/execall.py\')\"'
print 'To run all the examples, type \"fast=False; execfile(\'Examples/execall.py\')\"'
"

cd "$SCRIPT_PATH"
export PYTHONPATH="$SCRIPT_PATH/pypl:$PYTHONPATH"
PLATFORM="$(uname -s)"
case "$PLATFORM" in 
    Darwin)
        export DYLD_LIBRARY_PATH="$SCRIPT_PATH/pypl:$DYLD_LIBRARY_PATH"
        exec /usr/bin/python2.6 -i -c "$STARTUP_CMD"
        ;;
    Linux)
        dpkg -l |grep -q python-numpy || sudo apt-get install python-numpy
        export LD_LIBRARY_PATH="$SCRIPT_PATH/pypl:$LD_LIBRARY_PATH"
        exec /usr/bin/python -i -c "$STARTUP_CMD"
        ;;
esac
