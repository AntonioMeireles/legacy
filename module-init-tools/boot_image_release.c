/*
 *  boot_image_release - determines kernel release from /proc/cmdline
 *
 *  Copyright (c) 2007 rPath, Inc.
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

#include <asm/setup.h>
#include <sys/utsname.h>
#include <stdio.h>
#include <string.h>

/* Perhaps use a conary macro here and pull this from
   kernelpackage.recipe? */
#define BOOT_IMAGE_FILE_PREFIX "vmlinuz-"

#define BOOT_IMAGE_LEADER "BOOT_IMAGE="
#define CMDLINE "/proc/cmdline"

#ifndef COMMAND_LINE_SIZE
#define COMMAND_LINE_SIZE 256
#endif

/*
 *  Parses /proc/cmdline using the pattern:
 *
 *  ^.*[ \n\t]+BOOT_IMAGE=(.*\/)*vmlinuz-([^ \n\t]+)
 *
 *  where the ([^ \n\t]+) match after vmlinuz- is the return string.
 *
 *  Current failure mode is to bail (silently) on *any* anomaly to let
 *  the calling utility fall through to uname() for utsname info.
 */
int
boot_image_release (struct utsname *utsbuf)
{
  char cmdlinebuf[COMMAND_LINE_SIZE];
  FILE *cmdline;
  char *boot_image;
  char *release;

  if (!(cmdline = fopen (CMDLINE, "r")))
    return 1;

  if (fread (cmdlinebuf, sizeof (char), COMMAND_LINE_SIZE - 1, cmdline) < 1)
    return 1;

  if (!(boot_image = strtok (cmdlinebuf, " \n\t")))
    return 1;

  while (strncmp (boot_image, BOOT_IMAGE_LEADER, strlen (BOOT_IMAGE_LEADER)))
    if (!(boot_image = strtok (NULL, " \n\t")))
      return 1;

  if (!(release = strrchr (boot_image, '/')) &&
      !(release = strrchr (boot_image, '=')))
    return 1;

  if (strncmp (++release, BOOT_IMAGE_FILE_PREFIX,
	       strlen (BOOT_IMAGE_FILE_PREFIX)))
    return 1;

  if (!strlen (release += strlen (BOOT_IMAGE_FILE_PREFIX)))
    return 1;

  strncpy (utsbuf->release, release, _UTSNAME_VERSION_LENGTH);

  return 0;
}

#ifdef _TEST_BOOT_IMAGE_RELEASE_
int
main (void)
{
  struct utsname utsbuf;
  int retval = 0;

  retval = boot_image_release (&utsbuf);

  printf ("%s\n", retval ? "[not found]" : utsbuf.release);

  return retval;
}
#endif
