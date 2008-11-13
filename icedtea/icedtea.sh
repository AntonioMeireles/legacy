
CONF='/etc/sysconfig/java'

[ -f "$CONF" ] && source "$CONF"

[ ! -z "$JAVA" -a "$JAVA" != "%(javaname)s.%(targetarch)s" ] && {
    return
}

export JAVA_HOME="%(jdkhome)s"

echo "$PATH" | fgrep -q '%(jdkhome)s/jre/bin' || \
    export PATH="%(jdkhome)s/jre/bin:$PATH"

[ -d "%(jdkhome)s/bin" ] || return

echo "$PATH" | fgrep -q '%(jdkhome)s/bin' || \
    export PATH="%(jdkhome)s/bin:$PATH"

