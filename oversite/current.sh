#!/bin/bash
#
# Script used to get Foresight updates
#

# get some variables
if [ -f /etc/sysconfig/oversite ]; then
        . /etc/sysconfig/oversite
fi

if [ !$LOGFILE ]; then
	LOGFILE=/var/log/oversite
fi

if [ !$TODO ]; then
	TODO=/etc/oversite/todo
fi

if [[ "$AUTO" = yes && -f $TODO ]]
then
	for i in `cat /etc/oversite/todo`
	do
		conary update $i
	done
fi

if [[ "$AUTO" = yes  &&  $EXCEPT ]]
then
        /usr/bin/yuck --update --except $EXCEPT >> $LOGFILE 2>&1
elif [[ "$AUTO" = yes  && !$EXCEPT ]]
then
	/usr/bin/yuck --update
else
	echo "Auto update is disabled" >> $LOGFILE
fi
