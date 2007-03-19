from installclass import BaseInstallClass
from rhpl.translate import *
from constants import *
import os
import iutil

from autopart import getAutopartitionBoot, autoCreatePartitionRequests

class InstallClass(BaseInstallClass):
    hidden = 0
    
    id = "foresight"
    name = N_("f_oresight")
    pixmap = "rpath-color-graphic-only.png"
    description = N_("Foresight Linux install type.")

    sortPriority = 100
    showLoginChoice = 1

    def setSteps(self, dispatch):
        BaseInstallClass.setSteps(self, dispatch);
        if 'displayHelp' in dispatch.intf.__dict__:
            dispatch.intf.displayHelp = False
        dispatch.skipStep("checkdeps")
        dispatch.skipStep("package-selection")
        dispatch.skipStep("confirminstall")

    def setGroupSelection(self, grpset, intf):
        BaseInstallClass.__init__(self, grpset)
        grpset.unselectAll()
        grpset.selectGroup("everything")
