# less initialization script (csh)
if ( -x /usr/bin/lesspipe.sh ) then
  setenv LESSOPEN "|/usr/bin/lesspipe.sh %s"
endif

if ( $?LC_ALL ) then
  setenv LANGVAR $LC_ALL
else
  setenv LANGVAR $LANG
endif


if ( `echo $LANGVAR | cut -b 7- | tr -s "[:lower:]" "[:upper:]"` == "EUCJP" ) then
    setenv JLESSCHARSET japanese-euc
  else 
    if ( `echo $LANGVAR | cut -b 7- | tr -s "[:lower:]" "[:upper:]"` == "EUCKR" ) then
       setenv JLESSCHARSET korean
    endif
  endif
