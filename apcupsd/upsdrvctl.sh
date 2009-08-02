#!/bin/sh
# Pretend to be NUT, which the rPL halt script supports already.

case "$1" in
    shutdown)
        echo "Killing power at the UPS in 10 seconds ..."
        sleep 10
        /usr/sbin/apcupsd --killpower
        ;;
    *)
        echo "Dunno what $1 is"
        exit 1
        ;;
esac
