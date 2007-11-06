#
# user_gui.py: initial user creation dialog
#
# Copyright 2000-2007 Red Hat, Inc.
# Copyright (c) 2007 Elliot Peele <elliot@bentlogic.net>
#
# This software may be freely redistributed under the terms of the GNU
# library public license.
#
# You should have received a copy of the GNU Library Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

import gtk
import gobject
import re
import string
import gui
from iw_gui import *
from rhpl.translate import _, N_
from flags import flags

def handleCapsLockRelease(window, event, label):
    if event.keyval == gtk.keysyms.Caps_Lock and event.state & gtk.gdk.LOCK_MASK:
        if label.get_text() == "":
            label.set_text(_("<b>Caps Lock is on.</b>"))
            label.set_use_markup(True)
        else:
            label.set_text("")

class AccountWindow(InstallWindow):

    windowTitle = N_("Create Initial User")

    def getNext(self):
        def passwordError():
            self.pw.set_text("")
            self.confirm.set_text("")
            self.pw.grab_focus()
            raise gui.StayOnScreen

        def userError():
            self.user.set_text('')
            self.user.grab_focus()
            raise gui.StayOnScreen

        if(not self.__dict__.has_key("pw") or 
            not self.__dict__.has_key('user')):
            return None

        fullname = self.fullname.get_text()
        user = self.user.get_text()
        pw = self.pw.get_text()
        confirm = self.confirm.get_text()

        if not user:
            self.intf.messageWindow(_("Error with User"),
                                    _("You must enter an inital username."),
                                    custom_icon="error")
            userError()

        if not pw or not confirm:
            self.intf.messageWindow(_("Error with Password"),
                                    _("You must enter your password "
                                      "and confirm it by typing it a second "
                                      "time to continue."),
                                    custom_icon="error")
            passwordError()

        if pw != confirm:
            self.intf.messageWindow(_("Error with Password"),
                                    _("The passwords you entered were "
                                      "different.  Please try again."),
                                    custom_icon="error")
            passwordError()

        if len(pw) < 6:
            self.intf.messageWindow(_("Error with Password"),
                                    _("Your password must be at least "
                                      "six characters long."),
                                    custom_icon="error")
            passwordError()

        allowed = string.digits + string.ascii_letters + string.punctuation + " "
        for letter in pw:
            if letter not in allowed:
                self.intf.messageWindow(_("Error with Password"),
                                        _("Requested password contains "
                                          "non-ASCII characters, which are "
                                          "not allowed."),
                                        custom_icon="error")
                passwordError()

        self.initialUser['fullname'] = self.fullname.get_text()
        self.initialUser['name'] = self.user.get_text()
        self.initialUser['password'] = self.pw.get_text()
        self.initialUser['isCrypted'] = False
        return None

    def setFocus(self, area, data):
        self.user.grab_focus()

    # AccountWindow tag="accts"
    def getScreen(self, anaconda):
        self.initialUser = anaconda.id.initialUser
        self.intf = anaconda.intf

        self.capsLabel = gtk.Label()
        self.capsLabel.set_alignment(0.0, 0.5)

        self.intf.icw.window.connect("key-release-event",
                                     lambda w, e: handleCapsLockRelease(w, e,
                                     self.capsLabel))

        self.passwords = {}

        box = gtk.VBox()
        box.set_border_width(5)

        hbox = gtk.HBox()
        pix = gui.readImageFromFile("root-password.png")
        if pix:
            hbox.pack_start(pix, False)

        label = gui.WrappingLabel(_("This is the account that you will use to "
                                    "login to your computer."))
        label.set_line_wrap(True)
        label.set_size_request(350, -1)
        label.set_alignment(0.0, 0.5)
        hbox.pack_start(label, False)

        box.pack_start(hbox, False)

        table = gtk.Table(4, 2)
        table.set_size_request(365, -1)
        table.set_row_spacings(5)
        table.set_col_spacings(5)

        fullname = gui.MnemonicLabel(_("Full Name: "))
        fullname.set_alignment(0.0, 0.5)
        table.attach(fullname, 0, 1, 0, 1, gtk.FILL, 0, 10)
        user = gui.MnemonicLabel(_("User Name: "))
        user.set_alignment(0.0, 0.5)
        table.attach(user, 0, 1, 1, 2, gtk.FILL, 0, 10)
        pass1 = gui.MnemonicLabel(_("_Password: "))
        pass1.set_alignment(0.0, 0.5)
        table.attach(pass1, 0, 1, 2, 3, gtk.FILL, 0, 10)
        pass2 = gui.MnemonicLabel(_("_Confirm: "))
        pass2.set_alignment(0.0, 0.5)
        table.attach(pass2, 0, 1, 3, 4, gtk.FILL, 0, 10)

        self.fullname = gtk.Entry(128)
        fullname.set_mnemonic_widget(self.fullname)
        self.fullname.connect("activate", lambda widget, box=box: box.emit("focus",
                           gtk.DIR_TAB_FORWARD))
        self.fullname.connect("map-event", self.setFocus)
        self.fullname.set_visibility(True)
        self.user = gtk.Entry(128)
        user.set_mnemonic_widget(self.user)
        self.user.connect("activate", lambda widget,
                        box=box: box.emit("focus", gtk.DIR_TAB_FORWARD))
        self.user.connect("map-event", self.setFocus)
        self.user.set_visibility(True)

        self.pw = gtk.Entry(128)
        pass1.set_mnemonic_widget(self.pw)
        self.pw.connect("activate", lambda widget,
                        box=box: box.emit("focus", gtk.DIR_TAB_FORWARD))
        self.pw.connect("map-event", self.setFocus)
        self.pw.set_visibility(False)

        self.confirm = gtk.Entry(128)
        pass2.set_mnemonic_widget(self.confirm)
        self.confirm.connect("activate", lambda widget,
                             box=box: self.ics.setGrabNext(1))
        self.confirm.set_visibility(False)

        table.attach(self.fullname,  1, 2, 0, 1, gtk.FILL|gtk.EXPAND, 5)
        table.attach(self.user,      1, 2, 1, 2, gtk.FILL|gtk.EXPAND, 5)
        table.attach(self.pw,        1, 2, 2, 3, gtk.FILL|gtk.EXPAND, 5)
        table.attach(self.confirm,   1, 2, 3, 4, gtk.FILL|gtk.EXPAND, 5)
        table.attach(self.capsLabel, 1, 2, 4, 5, gtk.FILL|gtk.EXPAND, 5)

        hbox = gtk.HBox()
        hbox.pack_start(table, False)

        box.pack_start(hbox, False)

        # root password statusbar
        self.rootStatus = gtk.Label("")
        wrapper = gtk.HBox(0, False)
        wrapper.pack_start(self.rootStatus)
        box.pack_start(wrapper, False)

        if not self.initialUser['isCrypted']:
            self.pw.set_text(self.initialUser['password'])
            self.confirm.set_text(self.initialUser['password'])

        return box
