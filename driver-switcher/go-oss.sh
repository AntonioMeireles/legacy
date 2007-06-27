#!/bin/bash
#
# Copyright (c) 2007 Foresight Linux
# This file is distributed under the terms of the MIT License.
# A copy is available at http://www.rpath.com/permanent/mit-license.html
#
# Properly update to the open source video drivers
#

# Check for proper permissions
isRoot=`id -u`
if [ ! $isRoot == 0 ];
then
    echo "Must be run with escalated privileges, please try again with sudo"
    echo "example: sudo $0"
    exit
fi

echo -n "Are you sure you want to switch to the open source video drivers? (y/n)"
read confirm

if [ $confirm == "Y" ] || [ $confirm == "y" ];# || $confirm == "y" ];
then
    echo "Switching to the open source video driver"
    echo "This could a few minutes before providing feedback, please be patient"
    `conary update --interactive group-dist['!nvidia,!ati']`
    sed -i s/NO/YES/g /etc/sysconfig/reconfig
else
    echo "Cancelled"
fi
