/*
 *  grub-stage2-config - transfers configuration between stage2 loaders
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

/*
 * To-do:
 *
 * - Magic-number checks (aside from version-string matching)?
 * - Improve error handling for e.g. short reads.
 *
 */

#define WITHOUT_LIBC_STUBS
#include <config.h>
#include <shared.h>

#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>

#define NUM_SECTORS 2

static int nowrite = 0;
static int quiet = 0;
static int force = 0;
static char *optstring = "hnvq";
static struct option longopts[] =
{
  {"force", no_argument, 0, 'f'},
  {"help", no_argument, 0, 'h'},
  {"no-write", no_argument, 0, 'n'},
  {"version", no_argument, 0, 'v'},
  {"quiet", no_argument, 0, 'q'},
  {0}
};

static void
usage (int status)
{
  if (status)
    fprintf (stderr,
	     "Try ``grub-stage2-config --help'' for more information.\n");
  else
    printf ("Usage: grub-stage2-config [OPTION]... INFILE OUTFILE\n"
	    "Transfer the grub config-file path and LBA flag from INFILE to OUTFILE\n"
	    "\n"
	    "-h, --help                 display this help and exit\n"
	    "-v, --version              output version information and exit\n"
	    "-q, --quiet                suppress all normal output\n"
	    "-n, --no-write             don't write to destination file\n"
	    "    --force                ignore version-number mismatches\n"
	    "\n"
	    "Report bugs at http://issues.rpath.com/\n");

  exit (status);
}

int
main (int argc, char *argv[])
{
  int c;

  do
    {
      c = getopt_long (argc, argv, optstring, longopts, 0);
      switch (c)
	{
	case EOF:
	  break;

	case 'f':
	  force = 1;
	  break;

	case 'h':
	  usage (0);
	  break;

	case 'n':
	  nowrite = 1;
	  break;

	case 'v':
	  printf ("grub-stage2-config (GNU GRUB " VERSION ")\n");
	  exit (0);
	  break;

	case 'q':
	  quiet = 1;
	  break;

	default:
	  usage (1);
	  break;
	}
    }
  while (c != EOF);

  if (optind == argc - 2)
    {
      char inbuf[SECTOR_SIZE * NUM_SECTORS], outbuf[SECTOR_SIZE * NUM_SECTORS];
      FILE *infile, *outfile;
      char *inpart, *outpart;
      char *inconfig, *outconfig;
      char *inversion, *outversion;
      char *inlba, *outlba;

      if (!(infile = fopen (argv[optind], "r")))
	{
	  fprintf (stderr, "%s: fopen error (for reading): %s\n",
		   argv[optind], strerror (errno));
	  exit (1);
	}
      if (fread (inbuf, sizeof (char), SECTOR_SIZE * NUM_SECTORS, infile) !=
	  SECTOR_SIZE * NUM_SECTORS)
	{
	  fprintf (stderr, "%s: fread error: %s\n", argv[optind],
		   strerror (errno));
	  exit (1);
	}

      /*
       *  Everything but the block lists is found at the beginning of
       *  the second sector.
       */

      /* Four-byte install partition info. */
      inpart = inbuf + SECTOR_SIZE + STAGE2_INSTALLPART;
      /* One-byte force-lba flag. */
      inlba = inbuf + SECTOR_SIZE + STAGE2_FORCE_LBA;
      /* Start of version string.  (Not transferred!) */
      inversion = inbuf + SECTOR_SIZE + STAGE2_VER_STR_OFFS;
      inconfig = inversion;

      while (*(inconfig++));	/* Skip variable-length version string. */

      /* Now at config-file location string. */
      if (!quiet)
	{
	  int i;

	  printf ("Source stage2 version:           %s\n", inversion);

	  printf ("Using installation partition:    ");
	  for (i = 0; i < 4; i++)
	    printf ("%02hhx", (unsigned int)inpart[i]);

	  printf ("\n      force-lba flag:            %s\n",
		  *inlba ? "yes" : "no");
	  printf ("      config-file location:      %s\n\n", inconfig);
	}
      if (!(outfile = fopen (argv[++optind], "r+")))
	{
	  fprintf (stderr, "%s: fopen error (for reading/writing): %s\n",
		   argv[optind], strerror (errno));
	  exit (1);
	}
      if (fread (outbuf, sizeof (char), SECTOR_SIZE * NUM_SECTORS, outfile) !=
	  SECTOR_SIZE * NUM_SECTORS)
	{
	  fprintf (stderr, "%s: fread error: %s\n", argv[optind],
		   strerror (errno));
	  exit (1);
	}

      outpart = outbuf + SECTOR_SIZE + STAGE2_INSTALLPART;
      outlba = outbuf + SECTOR_SIZE + STAGE2_FORCE_LBA;
      outversion = outbuf + SECTOR_SIZE + STAGE2_VER_STR_OFFS;
      outconfig = outversion;

      while (*(outconfig++));	/* Skip version. */

      if (!quiet)
	{
	  int i;

	  printf ("Destination stage2 version:      %s\n", outversion);

	  printf ("Previous installation partition: ");
	  for (i = 0; i < 4; i++)
	    printf ("%02hhx", (unsigned int)outpart[i]);

	  printf ("\n         force-lba flag:         %s\n",
		  *outlba ? "yes" : "no");
	  printf ("         config-file location:   %s\n", outconfig);
	}
      if (strcmp (inversion, outversion))
	{
	  /* Don't honor --quiet here: this mismatch needs publicity! */
	  fprintf (stderr, "*** %s: stage2 version mismatch: source %s,"
		   " destination %s\n",
		   force ? "WARNING" : "FATAL ERROR", inversion, outversion);
	  fprintf (stderr, "(You should probably run grub-install.)\n");

	  if (!force)
	    exit (1);
	}

      /* Transfer install partition info. */
      while (outpart < outbuf + SECTOR_SIZE + STAGE2_INSTALLPART + 4)
	*(outpart++) = *(inpart++);

      /* Transfer force-lba flag. */
      *outlba = *inlba;

      /* Transfer config-file location. */
      while (outconfig < outbuf + (SECTOR_SIZE * NUM_SECTORS) && *inconfig)
	*(outconfig++) = *(inconfig++);

      *outconfig = 0;

      /*
       *  End of first sector has block lists...listed backwards (sort
       *  of) in 8-byte (BOOTSEC_LISTSIZE) groups.  Copy through the
       *  first empty group found.
       *
       *  (Note that block lists are not needed in stage2, only in 1.5.)
       */
#if 0
      {
	char *inblocks = inbuf + SECTOR_SIZE;
	char *outblocks;
	int mask;
	int blockbytes = 0;

	if (!quiet)
	  printf ("\nTransferring block list (shown in reverse order)...\n   ");

	do
	  {
	    mask = 0;

	    do
	      {
		mask |= *(--inblocks);
		if (!quiet)
		  printf ("%02hhx ", (unsigned int)*(inblocks));
	      }
	    while (++blockbytes % BOOTSEC_LISTSIZE);

	    if (!quiet)
	      printf ("\n   ");
	  }
	while (mask);

	if (!quiet)
	  printf ("\nCopied %d block lists", blockbytes / BOOTSEC_LISTSIZE);

	outblocks = outbuf + SECTOR_SIZE - blockbytes;

	assert (((inblocks - inbuf) == (outblocks - outbuf)) && !mask);

	/* Transfer the block lists */
	while (outblocks < outbuf + SECTOR_SIZE)
	  {
	    *(outblocks++) = *(inblocks++);
	    ++mask;		/* Reuse mask as sanity counter. */
	  }
	if (!quiet)
	  printf (" (%d bytes).\n", mask);
      }
#endif	/* 0 -- transferring block lists disabled by default */

      /*
       *  Done transferring information.
       */

      /* Rewind output file. */
      if (fseek (outfile, 0, SEEK_SET) != 0)
	{
	  fprintf (stderr, "%s: fseek error: %s\n", argv[optind],
		   strerror (errno));
	  exit (1);
	}
      if (!nowrite)
	/* Rewrite NUM_SECTORS, with embedded changes. */
	if (fwrite (outbuf, sizeof (char), SECTOR_SIZE * NUM_SECTORS, outfile)
	    != SECTOR_SIZE * NUM_SECTORS)
	  {
	    fprintf (stderr, "%s: fwrite error: %s\n", argv[optind],
		     strerror (errno));
	    exit (1);
	  }
    }
  else
    {
      usage (1);
    }
  return 0;
}
