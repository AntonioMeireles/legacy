#
# user_text.py: text mode initial user setup
#
# Copyright 2000-2002 Red Hat, Inc.
# Copyright (c) 2007 Elliot Peele <elliot@bentlogic.net>
#
# This software may be freely redistributed under the terms of the GNU
# library public license.
#
# You should have received a copy of the GNU Library Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

from snack import *
from constants_text import *
from rhpl.translate import _

def has_bad_chars(pw):
    allowed = string.digits + string.ascii_letters + string.punctuation + " "
    for letter in pw:
        if letter not in allowed:
            return 1
    return 0

class InitialUserWindow:
    def __call__ (self, screen, anaconda):
        toplevel = GridFormHelp(screen, _("Create Initial User"), "rootpw", 1, 3)

        if anaconda.id.initialUser["isCrypted"]:
            anaconda.id.initialUser["password"] = ""

        fullnameEntry = Entry(24, text = anaconda.id.initialUser['fullname'])
        userEntry = Entry(24, text = anaconda.id.initialUser['name'])
        entry1 = Entry(24, password = 1, text = anaconda.id.initialUser["password"])
        entry2 = Entry(24, password = 1, text = anaconda.id.initialUser["password"])
        passgrid = Grid (2, 4)
        passgrid.setField(Label(_('Full Name:')), 0, 0, (0, 0, 1, 0), anchorLeft = 1)
        passgrid.setField(Label(_('Username:')), 0, 1, (0, 0, 1, 0), anchorLeft = 1)
        passgrid.setField(Label(_("Password:")), 0, 2, (0, 0, 1, 0), anchorLeft = 1)
        passgrid.setField(Label(_("Password (confirm):")), 0, 3, (0, 0, 1, 0), anchorLeft = 1)
        passgrid.setField(fullnameEntry, 1, 0)
        passgrid.setField(userEntry, 1, 1)
        passgrid.setField(entry1, 1, 2)
        passgrid.setField(entry2, 1, 3)
        toplevel.add(passgrid, 0, 1, (0, 0, 0, 1))

        bb = ButtonBar(screen, (TEXT_OK_BUTTON, TEXT_BACK_BUTTON))
        toplevel.add(bb, 0, 2, growx = 1)

        while 1:
            toplevel.setCurrent(userEntry)
            result = toplevel.run()
            rc = bb.buttonPressed(result)
            if rc == TEXT_BACK_CHECK:
                screen.popWindow()
                return INSTALL_BACK
            if len(userEntry.value()) < 3:
                ButtonChoiceWindow(sceen, _("Username Length"),
                       _("Your username must be at least 3 charactures in "
                         "long."),
                       buttons = [ TEXT_OK_BUTTON ], width = 50)
            if len(entry1.value()) < 6:
                ButtonChoiceWindow(screen, _("Password Length"),
                       _("Your password must be at least 6 characters "
                         "long."),
                       buttons = [ TEXT_OK_BUTTON ], width = 50)
            elif entry1.value() != entry2.value():
                ButtonChoiceWindow(screen, _("Password Mismatch"),
                       _("The passwords you entered were different. Please "
                         "try again."),
                       buttons = [ TEXT_OK_BUTTON ], width = 50)
            elif has_bad_chars(entry1.value()):
                ButtonChoiceWindow(screen, _("Error with Password"),
                       _("Requested password contains non-ASCII characters, "
                         "which are not allowed."),
                       buttons = [ TEXT_OK_BUTTON ], width = 50)
            else:
                break

            userEntry.set('')
            entry1.set('')
            entry2.set('')

        screen.popWindow()
        anaconda.id.initialUser['fullname'] = fullnameEntry.value()
        anaconda.id.initialUser['name'] = userEntry.value()
        anaconda.id.initialUser["password"] = entry1.value()
        anaconda.id.initialUser["isCrypted"] = False
        return INSTALL_OK
