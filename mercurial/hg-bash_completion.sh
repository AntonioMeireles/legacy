if [ "$PS1" ]; then
  D="/etc/bash_completion.d"
  if [ -f "$D"/git ]; then
    . "$D"/git
  fi
  unset D
fi
