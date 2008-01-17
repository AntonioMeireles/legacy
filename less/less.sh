# less initialization script (sh)
[ -x /usr/bin/lesspipe.sh ] && export LESSOPEN="|/usr/bin/lesspipe.sh %s"

if [ x"$LC_ALL" != "x" ]; then 
  LANGVAR=$LC_ALL
else
  LANGVAR=$LANG
fi

if [ x`echo $LANGVAR | cut -b 7- | tr -s "[:lower:]" "[:upper:]"` = x"EUCJP" ]; then
        export JLESSCHARSET=japanese-euc
elif [ x`echo $LANGVAR | cut -b 7- | tr -s "[:lower:]" "[:upper:]"` = x"EUCKR" ]; then
        export JLESSCHARSET=korean
fi
