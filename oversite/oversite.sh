#!/bin/bash
#
# Script used to get Foresight updates
#

# get some variables
if [ -f /etc/sysconfig/oversite ]; then
        . /etc/sysconfig/oversite
fi

if [ -z $LOGFILE ]; then
	LOGFILE=/var/log/oversite
fi

if [ -z $TASKS ]; then
	TASKS=/etc/oversite/tasks
fi

if [ -z $DISTID ]; then
        DISTID=1
fi

if [ -z $SYSID ]; then
	wget http://oversite.foresightlinux.com/register.php?distid=$DISTID -O /tmp/sysid
	. /tmp/sysid
	cat /tmp/sysid >> /etc/sysconfig/oversite
	#rm /tmp/sysid
fi

if [[  $SYSID && $AUTO = yes ]]; then
        wget "http://oversite.foresightlinux.com/checkin.php?sysid=$SYSID&distid=$DISTID" -O $TASKS
fi

if [[ $AUTO = yes && -f $TASKS ]]
then
	echo "begin `date`..." >> $LOGFILE 2>&1
	for i in `cat /etc/oversite/tasks`
	do
		conary update $i >> $LOGFILE 2>&1
	done
	rm -f $TASKS
	echo "end `date`..." >> $LOGFILE 2>&1
fi

if [[ $AUTO = yes  &&  $EXCEPT ]]
then
        /usr/bin/yuck --update --except $EXCEPT >> $LOGFILE 2>&1
elif [[ $AUTO = yes  && !$EXCEPT ]]
then
	/usr/bin/yuck --update
else
	echo "Auto update is disabled" >> $LOGFILE
fi
