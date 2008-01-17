/* ----------------------------------------------------------------------- *
 *   
 *   Copyright 2007 rPath, Inc. - All Rights Reserved
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, Inc., 53 Temple Place Ste 330,
 *   Boston MA 02111-1307, USA; either version 2 of the License, or
 *   (at your option) any later version; incorporated herein by reference.
 *
 * ----------------------------------------------------------------------- */

/*
 * ext3flush
 *
 * Force an ext3 filesystem to flush its log by bmapping any file on the
 * filesystem.
 *
 */

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <sysexits.h>
#include <sys/ioctl.h>
#include <linux/fs.h>		/* FIBMAP */

static int flush_file(const char *filename)
{
	unsigned int blk;
	int fd, rv;

	fd = open(filename, O_RDONLY);
	if (fd < 0)
		return -1;

	blk = 0;
	rv = ioctl(fd, FIBMAP, &blk);
	close(fd);

	return rv;
}

int main(int argc, char *argv[])
{
	int i;

	if (argc < 2) {
		fprintf(stderr, "Usage: %s filename...\n", argv[0]);
		return EX_USAGE;
	}

	for (i = 1; i < argc; i++) {
		if (flush_file(argv[i])) {
			int err = errno;
			fprintf(stderr, "%s: %s: %s\n",
				argv[0], argv[i], strerror(err));
			return (errno == EPERM) ? EX_NOPERM : EX_OSERR;
		}
	}

	return 0;
}
