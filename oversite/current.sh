#!/bin/bash

conary update abiword
conary update gnome-backgrounds
/usr/bin/yuck --update --except kernel,xorg-x11,xorg-x11-fonts,xorg-x11-tools,xorg-x11-xfs,conary >> /var/log/oversite 2>&1
