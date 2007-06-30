#!/usr/bin/python

# Banshee Plugin for Xchat
# Copyright (C) 2007  Will Farrington <wcfarrington@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import xchat
import dbus

__module_name__ = "Banshee Plugin for Xchat"
__module_version__ = "1.0"
__module_description__ = "Announce music from and control Banshee Music Player."

bus = dbus.SessionBus()

class Dbus:
    def __init__(self):
        obj = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
        iface = dbus.Interface(obj, 'org.freedesktop.DBus')
        if 'org.gnome.Banshee' in iface.ListNames():
            banshee_obj = bus.get_object('org.gnome.Banshee', '/org/gnome/Banshee/Player')
            global banshee_iface
            banshee_iface = dbus.Interface(banshee_obj, 'org.gnome.Banshee.Core')
        else:
            xchat.prnt("\002Banshee is not registered with DBus. Please start Banshee.\002")
            return
    
    def grab_track_data(self):
        global track_title
        global track_artist
        global track_album
        global track_rating
        global track_pos
        global track_dur
        
        track_title = banshee_iface.GetPlayingTitle()
        track_artist = banshee_iface.GetPlayingArtist()
        track_album = banshee_iface.GetPlayingAlbum()
        track_rating = banshee_iface.GetPlayingRating()
        track_pos = banshee_iface.GetPlayingPosition()
        track_dur = banshee_iface.GetPlayingDuration()
        
        if track_rating == 0:
            track_rating = "Not Rated."
        else:
            track_rating = "%s/5" % track_rating
            
        track_pos = int(track_pos)
        track_dur = int(track_dur)
        track_pos = "%d:%02d" % (track_pos / 60, track_pos % 60)
        track_dur = "%d:%02d" % (track_dur / 60, track_dur % 60)

class Commands:
    def mabout(self, word, word_eol, nil):
        xchat.prnt("\002\037%s\037\002" % __module_name__)
        xchat.prnt(" \002About:\002")
        xchat.prnt(" * Author: Will Farrington <wcfarrington@gmail.com>")
        xchat.prnt(" * Script Version: %s" % __module_version__)
        xchat.prnt(" \002Help:\002")
        xchat.prnt(" * \037/media\037 - Displays the currently playing track")
        xchat.prnt(" * \037/prev\037 - Skips to the previous track")
        xchat.prnt(" * \037/stop\037 - Stops playback")
        xchat.prnt(" * \037/play\037 - Starts playback")    
        xchat.prnt(" * \037/pause\037 - Pauses playback")
        xchat.prnt(" * \037/next\037 - Skips to the next track")
        xchat.prnt(" * \037/rate n\037 - Rates the song n/5")
        
    def media(self, word, word_eol, nil):
        Dbus().grab_track_data()
        xchat.command("me is listening to: \"%s\" by %s on %s; Rated: %s (%s/%s)" % (track_title, track_artist, track_album, track_rating, track_pos, track_dur))
        
    def next(self, word, word_eol, nil):
        Dbus()
        banshee_iface.Next()
        xchat.prnt("Skipped to next track.")
        
    def prev(self, word, word_eol, nil):
        Dbus()
        banshee_iface.Previous()
        xchat.prnt("Skipped to previous track.")
    
    def play(self, word, word_eol, nil):
        Dbus()
        banshee_iface.Play()
        xchat.prnt("Started playback.")
    
    def pause(self, word, word_eol, nil):
        Dbus()
        banshee_iface.Pause()
        xchat.prnt("Paused playback.")
        
    def rate(self, word, word_eol, new_rating):
        Dbus().grab_track_data()
        new_rating = int(word[1])
        banshee_iface.SetPlayingRating(new_rating)
        xchat.prnt("Rated \"%s\" by %s a %s/5." % (track_title, track_artist, new_rating))

xchat.prnt("Loaded \002%s\002:" % __module_name__)
xchat.prnt("Use \002/mabout\002 to display a list of commands.")

mabout_hook = xchat.hook_command("mabout", Commands().mabout)
media_hook  = xchat.hook_command("media", Commands().media)
next_hook   = xchat.hook_command("next", Commands().next)
prev_hook   = xchat.hook_command("prev", Commands().prev)
play_hook   = xchat.hook_command("play", Commands().play)
pause_hook  = xchat.hook_command("pause", Commands().pause)
rate_hook   = xchat.hook_command("rate", Commands().rate)
        
def munload(nil):
    xchat.unhook(mabout_hook)
    xchat.unhook(media_hook)
    xchat.unhook(next_hook)
    xchat.unhook(prev_hook)
    xchat.unhook(play_hook)
    xchat.unhook(pause_hook)
    xchat.unhook(rate_hook)
    xchat.prnt("Thanks for using my script! =)")

xchat.hook_unload(munload)
