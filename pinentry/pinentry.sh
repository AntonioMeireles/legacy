#!/bin/bash

[ -x %(bindir)s/pinentry-gtk-2 ] && exec %(bindir)s/pinentry-gtk-2 "$@"
exec %(bindir)s/pinentry-curses "$@"
