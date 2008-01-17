#
# Makefile for mod_auth_shadow
#
# 'make all' must be run as root, in order
#   to create an suid root binary.
#

APXS = /usr/sbin/apxs
CC = gcc
DEFINES = -D INSTBINDIR=\\\"$(DESTDIR)$(BINDIR)\\\"

all: validate .libs/mod_auth_shadow.so

install:
	chown root:root validate
	chmod +s validate
	cp validate $(DESTDIR)$(BINDIR)/validate
	$(APXS) -i -a -n auth_shadow mod_auth_shadow.la

clean: 
	rm -rf validate mod_auth_shadow.so testvalidate *.o *.lo *.slo *.la .libs

test: testvalidate

validate: validate.o
	$(CC) validate.o -lcrypt -o validate

validate.o: validate.c validate.h
	$(CC) -c validate.c

testvalidate.o: testvalidate.c
	$(CC) -c testvalidate.c

testvalidate: testvalidate.o
	$(CC) testvalidate.o -o testvalidate

.libs/mod_auth_shadow.so: mod_auth_shadow.c validate.h
	$(APXS) $(DEFINES) -c mod_auth_shadow.c

