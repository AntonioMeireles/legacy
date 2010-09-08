if [ "$PS1" ]; then
  # the bzr completion script needs this
  shopt -s extglob
  D="/etc/bash_completion.d"
  if [ -f "$D"/bzr ]; then
    . "$D"/bzr
  fi
fi

