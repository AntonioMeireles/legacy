#!/bin/bash
#
# Script to check database version (Sqlite 2 or 3) and
# convert if necessary

RETVAL=0

if [ -f $HOME/.gnome2/f-spot/photos.db ];
then
    ver=`file $HOME/.gnome2/f-spot/photos.db |grep "Version 3"`
    RETVAL=$?
fi

if [ $RETVAL != 0 ];
then
    echo "Converting the F-Spot photo database"
    mv $HOME/.gnome2/f-spot/photos.db $HOME/.gnome2/f-spot/photos.db.v2
    echo .dump | sqlite $HOME/.gnome2/f-spot/photos.db.v2 | sqlite3 $HOME/.gnome2/f-spot/photos.db
fi

