#! /bin/bash
#
# udevd:  udev daemon
#
# chkconfig: 345 10 12
# description:  This is a daemon for collecting and maintaing information \
#               about hardware from several sources. \
#               creating devices nodes and sending info to hal daemon
#
# processname: udevd
# pidfile: /var/run/udevd.pid


case "$1" in
start)
	/sbin/udevd --daemon
	;;
stop)
	pkill udevd
	;;
*)
	echo $0 "start|stop"
	;;
esac
