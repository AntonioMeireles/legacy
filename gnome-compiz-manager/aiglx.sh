#!/bin/bash                                                                     
X=`glxinfo | grep GLX_EXT_texture_from_pixmap`
Y=`xdpyinfo | grep Composite`
if [ -n "$X" ]; then
    if [ -n "$Y" ]; then
    
        echo "compiz capable" # put compiz as default wm in gconf               
        /usr/bin/compiz-tray-icon
    else
        echo "*NOT* compiz capable" # do nothing                                
    fi
else
    echo "*NOT* compiz capable" # do nothing                                    
fi