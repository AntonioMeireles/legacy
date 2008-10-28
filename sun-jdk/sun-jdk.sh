
CONF='/etc/sysconfig/java'

[ -f "$CONF" ] && source "$CONF"

[ ! -z "$JAVA" -a "$JAVA" != "%(javaname)s.%(targetarch)s" ] && {
    exit 0
}

export JAVA_HOME="%(jdkhome)s"

echo "$PATH" | fgrep -q '%(jdkhome)s/jre/bin' || \
    export PATH="%(jdkhome)s/jre/bin:$PATH"

[ -d "%(jdkhome)s/bin" ] || exit 0

echo "$PATH" | fgrep -q '%(jdkhome)s/bin' || \
    export PATH="%(jdkhome)s/bin:$PATH"
echo "$MANPATH" | fgrep -q '%(jdkhome)s/jre/man' || \
    export MANPATH=`echo "%(jdkhome)s/man:$MANPATH" | sed -r 's/:$//'`

