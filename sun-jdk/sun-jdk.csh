
set JAVA=''

set CONF='/etc/sysconfig/java.csh'

if ( -f "$CONF" ) then
    source "$CONF"
endif

if ( $JAVA != '' ) then
    if ( "$JAVA" != "%(javaname)s.%(targetarch)s" ) then
        exit 0
    endif
endif

setenv JAVA_HOME "%(jdkhome)s"

if ( `echo "$PATH" | fgrep '%(jdkhome)s/jre/bin' | wc -l` == "0" ) then
    setenv PATH "%(jdkhome)s/jre/bin:$PATH"
endif

if ( -d "%(jdkhome)s/bin" ) then

    if ( `echo "$PATH" | fgrep '%(jdkhome)s/bin' | wc -l` == "0" ) then
        setenv PATH "%(jdkhome)s/bin:$PATH"
    endif

    if ( $?MANPATH ) then
        if ( `echo "$MANPATH" | fgrep '%(jdkhome)s/man' | wc -l` == "0" ) then
            setenv MANPATH "%(jdkhome)s/man:$MANPATH"
        endif
    else
        setenv MANPATH "%(jdkhome)s/man"
    endif
endif

