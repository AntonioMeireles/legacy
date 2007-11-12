#
# Copyright 2007 Elliot Peele <elliot@bentlogic.net>
#

import sys
sys.path.append('/usr/lib/anaconda/installclasses')

import rpathbase
from constants import *
from rhpl.translate import *

class InstallClass(rpathbase.InstallClass):
    hidden = 0

    id = "foresight"
    name = N_("foresight")
    pixmap = "rpath-color-graphic-only.png"
    description = N_("Foresight Linux install type.")

    sortPriority = 40000
    showLoginChoice = 1

    def setSteps(self, anaconda):
        rpathbase.InstallClass.setSteps(self, anaconda);
        anaconda.dispatch.skipStep("accounts")
        anaconda.dispatch.skipStep("group-selection")
        #anaconda.dispatch.skipStep("postselection")
        #anaconda.dispatch.skipStep("confirminstall")
