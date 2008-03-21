#!/bin/sh

##
## Variables
##
MOZ_ARCH=$(uname -m)
case $MOZ_ARCH in
    x86_64 | ia64 | s390 )
    MOZ_LIB_DIR="/usr/lib64"
    SECONDARY_LIB_DIR="/usr/lib"
    ;;
    * )
    MOZ_LIB_DIR="/usr/lib"
    SECONDARY_LIB_DIR="/usr/lib64"
    ;;
esac


##
## Select the propper plugin dir
## Wrapped plug-ins are located in /lib/mozilla/plugins-wrapped
##
if [ -x "/usr/bin/mozilla-plugin-config" ]
then
  MOZ_PLUGIN_DIR="plugins-wrapped"
else
  MOZ_PLUGIN_DIR="plugins"
fi

##
## Make sure that we set the plugin path
##

MOZ_PLUGIN_PATH=$MOZ_LIB_DIR/xulrunner/$MOZ_PLUGIN_DIR:$MOZ_LIB_DIR/xulrunner/plugins

export MOZ_PLUGIN_PATH

