# less initialization script (sh)
[ -x /usr/bin/lesspipe.sh ] && LESSOPEN="|/usr/bin/lesspipe.sh %s" && export LESSOPEN

if [ x"$LC_ALL" != "x" ]; then 
  LANGVAR=$LC_ALL
else
  LANGVAR=$LANG
fi

if [ x`echo $LANGVAR | cut -b 7- | tr -s "[:lower:]" "[:upper:]"` = x"EUCJP" ]; then
        JLESSCHARSET=japanese-euc
        export JLESSCHARSET
elif [ x`echo $LANGVAR | cut -b 7- | tr -s "[:lower:]" "[:upper:]"` = x"EUCKR" ]; then
        JLESSCHARSET=korean
        export JLESSCHARSET
fi
