#
# users.py:  Code for creating user accounts and setting the root password
#
# Chris Lumens <clumens@redhat.com>
#
# Copyright (c) 2006, 2007 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
import libuser
import string
import crypt
import random
import tempfile
import os
import os.path

def createLuserConf(instPath):
    """Writes a libuser.conf for instPath."""
    (fd, fn) = tempfile.mkstemp(prefix="libuser.")
    buf = """
[defaults]
skeleton = %(instPath)s/etc/skel
mailspooldir = %(instPath)s/var/mail
crypt_style = md5
modules = files shadow
create_modules = files shadow
[files]
directory = %(instPath)s/etc
[shadow]
directory = %(instPath)s/etc
""" % {"instPath": instPath}
    os.write(fd, buf)
    os.close(fd)

    os.environ["LIBUSER_CONF"] = fn

def cryptPassword(password, useMD5):
    if useMD5:
	salt = "$1$"
	saltLen = 8
    else:
	salt = ""
	saltLen = 2

    for i in range(saltLen):
	salt = salt + random.choice (string.letters +
                                     string.digits + './')

    return crypt.crypt (password, salt)

class Users:
    def __init__ (self):
        self.admin = libuser.admin()

    def createUser (self, name, password=None, isCrypted=False, groups=[],
                    homedir=None, shell=None, uid=None, lock=False,
                    fullname=None, root="/mnt/sysimage"):
        if self.admin.lookupUserByName(name):
            return None

        userEnt = self.admin.initUser(name)
        groupEnt = self.admin.initGroup(name)

        gidLst = map(lambda grp: grp.get(libuser.GIDNUMBER)[0],
                     filter(lambda grp: grp,
                            map(lambda name: self.admin.lookupGroupByName(name), groups)))
        gidLst.extend(groupEnt.get(libuser.GIDNUMBER))

        userEnt.set(libuser.GIDNUMBER, gidLst)

        if not homedir:
            homedir = "/home/" + name

        # Do this to make the user's home dir under the install root.
        if homedir[0] != "/":
            userEnt.set(libuser.HOMEDIRECTORY, root + "/" + homedir)
        else:
            userEnt.set(libuser.HOMEDIRECTORY, root + homedir)

        if fullname:
            userEnt.set(libuser.GECOS, fullname)

        if shell:
            userEnt.set(libuser.LOGINSHELL, shell)

        if uid >= 0:
            userEnt.set(libuser.UIDNUMBER, uid)

        self.admin.addUser(userEnt)
        self.admin.addGroup(groupEnt)

        if password:
            if isCrypted:
                self.admin.setpassUser(userEnt, password, isCrypted)
            else:
                self.admin.setpassUser(userEnt, cryptPassword(password, True), True)

        if lock:
            self.admin.lockUser(userEnt)

        # Now set the correct home directory to fix up passwd.
        userEnt.set(libuser.HOMEDIRECTORY, homedir)
        self.admin.modifyUser(userEnt)

        # Add the user to the wheel group
        self.addToWheelGroup(name)

    def setRootPassword(self, password, isCrypted, useMD5, lock):
        rootUser = self.admin.lookupUserByName("root")

        if isCrypted:
            self.admin.setpassUser(rootUser, password, True)
        else:
            self.admin.setpassUser(rootUser, cryptPassword(password, useMD5), True)

        if lock:
            self.admin.lockUser(rootUser)

        self.admin.modifyUser(rootUser)

    def addToWheelGroup(self, name):
        groupEnt = self.admin.lookupGroupByName('wheel')

        members = groupEnt.get(libuser.MEMBERNAME)
        if not members:
           members = []

        members.append(name)
        groupEnt.set(libuser.MEMBERNAME, members)
        self.admin.modifyGroup(groupEnt)
