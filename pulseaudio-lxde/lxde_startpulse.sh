#!/bin/sh
pulseaudio --kill
pulseaudio -D --high-priority --start
pactl load-module module-x11-xsmp
