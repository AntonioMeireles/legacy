if [ "$PS1" ]; then
  D="/etc/bash_completion.d"
  if [ -f "$D"/svn ]; then
    . "$D"/svn
  fi
  unset D
fi
