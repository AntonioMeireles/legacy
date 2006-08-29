#!/bin/bash
#
# Script to check database version (Sqlite 2 or 3) and
# convert if necessary

ver=`file .gnome2/f-spot/photos.db |grep "Version 3"`
RETVAL=$?
if [ $RETVAL != 0 ];
then
    echo $RETVAL
    echo "Converting the F-Spot photo database"
    mv ~/.gnome2/f-spot/photos.db ~/.gnome2/f-spot/photos.db.v2
    echo .dump | sqlite .gnome2/f-spot/photos.db.v2 | sqlite3 ~/.gnome2/f-spot/photos.db
fi

