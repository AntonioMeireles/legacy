#!/bin/bash
X=`glxinfo | grep GLX_EXT_texture_from_pixmap`
if [ -n "$X" ]; then
    echo "compiz capable" # put compiz as default wm in gconf
    /usr/bin/compiz-tray-icon
else
    echo "*NOT* compiz capable" # do nothing
fi
