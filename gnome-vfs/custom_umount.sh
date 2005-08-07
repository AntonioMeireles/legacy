#! /bin/sh
DEV=$(grep $1 /etc/mtab |grep -o '^[^" "]*')
pumount $1
echo $DEV
eject $DEV
