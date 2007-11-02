#
# Copyright (c) 2007 rPath, Inc.
# All rights reserved
#

import os.path

from rhpl.translate import _

from conary.lib import util

import logging
from constants import *
from flags import flags
from tarextract import *
from tarcallbacks import ProgressCallback
from installmethod import FileCopyException
from rpathbackendbase import rPathBackendBase
from product import productPackagePath, productPath

log = logging.getLogger('anaconda')

class TarBackend(rPathBackendBase):
    def __init__(self, method, instPath):
        rPathBackendBase.__init__(self, method, instPath)

        self.supportsUpgrades = False
        self.supportsPackageSelection = False

    def doInitialSetup(self, anaconda):
        rPathBackendBase.doInitialSetup(self, anaconda)
        self.comps = TarComps(self.method, anaconda.intf)

    def doRepoSetup(self, anaconda):
        if anaconda.dir == DISPATCH_BACK:
            return

        # Don't reprocess package data.
        if self.comps.chunks:
            return

        self.comps.processPackageData()

    def doInstall(self, anaconda):
        if flags.test:
            return

        totalSize = 0
        for chunk in self.comps.chunks:
            totalSize += chunk.size

        instProgress = ProgressCallback(anaconda, len(self.comps), totalSize)

        util.settempdir(self.instPath + '/var/tmp')
        te = TarExtractor(self.instPath, progress=instProgress)

        for chunk in self.comps.chunks:
            # Try to retreive tarball chunk.
            while True:
                try:
                    # Make sure to use the correct disc.
                    self.method.switchMedia(chunk.disc)
                    fn = self.method.getFilename('%s/%s' %
                            (productPackagePath, chunk.fn))
                    break
                except FileCopyException:
                    self.method.unmountCD()
                    anaconda.intf.messageWindow(_("Error"),
                        _("The file %s cannot be opened. This is due "
                          "to a missing or corrupt file.  "
                          "If you are installing from CD media this usually "
                          "means the CD media is corrupt, or the CD drive is "
                          "unable to read the media.\n\n"
                          "Press <return> to try again.") % chunk.fn)

            log.info('installing %s' % chunk.fn)

            # Extract chunk
            te.extractFile(fn)

        te.done()
        anaconda.id.instProgress = None
        self.method.filesDone()

    def doPostInstall(self, anaconda):
        rPathBackendBase.doPostInstall(self, anaconda)

        if os.path.exists(self.instPath + '/boot/grub/device.map'):
            os.unlink(self.instPath + '/boot/grub/device.map')

        # start in run level 5 if xdm is installed
        if os.path.exists(self.instPath + '/usr/bin/xdm'):
            anaconda.id.desktop.setDefaultRunLevel(5)

    def getRequiredMedia(self):
        return self.comps.getRequiredMedia()


class TarComps(object):
    def __init__(self, method, intf):
        self.method = method
        self.intf = intf
        self.tbListFile = None
        self.chunks = []

    def __len__(self):
        return len(self.chunks)

    def _getFiles(self):
        log.info('copying needed files')
        # If using a cd imstall make sure we are on disc 1
        self.method.switchMedia(1)

        self.tbListFile = self.method.getFilename(productPath + '/base/tblist')

    def _parseTbList(self):
        log.info('parsing tblist')
        for i, line in enumerate(open(self.tbListFile).readlines()):
            line = line.strip()
            parts = line.split()
            if len(parts) != 3:
                log.warn('invalid line in tblist: %s' % (line,))
                continue
            chunkfile, size, disc = parts
            size = long(size)
            disc = int(disc)

            chunk = TarChunk(chunkfile, size, disc)
            self.chunks.append(chunk)

    def processPackageData(self):
        title = _('Parsing Package Data')

        win = self.intf.waitWindow(title,
                    _('Copying needed files...'))

        self._getFiles()

        win.pop()
        win = self.intf.waitWindow(title,
                    _('Parsing Changeset List...'))

        self._parseTbList()

        win.pop()

    def getRequiredMedia(self):
        discs = []
        for chunk in self.chunks:
            if chunk.disc not in discs:
                discs.append(chunk.disc)
        return discs


class TarChunk(object):
    __slots__ = ('fn', 'size', 'disc')

    def __init__(self, fn, size, disc):
        self.fn = fn
        self.size = size
        self.disc = disc
