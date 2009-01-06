;;; loaded before user's ".emacs" file and default.el

;; load ".el" files in "%(datadir)s/%(name)s/site-lisp/site-start.d/" on startup
(mapc 'load
      (directory-files "%(datadir)s/%(name)s/site-lisp/site-start.d"
		       t "\\.el\\'"))
