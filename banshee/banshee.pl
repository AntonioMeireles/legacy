#!/usr/bin/perl -w



# XChat-Banshee-Plugin v1.4
#
# Author: Will Farrington <wcfarrington@gmail.com>

#

# This program is free software; you can redistribute it and/or modify

# it under the terms of the GNU General Public License as published by

# the Free Software Foundation; either version 2 of the License, or

# (at your option) any later version.

#

# This program is distributed in the hope that it will be useful,

# but WITHOUT ANY WARRANTY; without even the implied warranty of

# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the

# GNU General Public License for more details.


# This script allows the user to control Banshee and print playing media from Xchat. It was written over the course of several weeks. As such there are a few coding guidelines I ask if anyone wants to submit revisions to the code:

# Comments are required. Comments describing a subroutine should be prefaced with "##" and entirely capitalized, while comments inside a subroutine or not describing one should use "#" and be in traditional sentence form.

# Extra linebreaks are appreciated but not required.

# When the user submits ANY command, the script should offer in-Xchat feedback about that command.

# When at all possible, DBUS should be preferred over any sort of BASH command flag.


use Net::DBus;


# Register the plugin in Xchat.


$script_name = "XChat-Banshee Plugin";

$script_version = "1.4";

$script_description = "Integrates XChat with Banshee - GNOME Media Player.";



Xchat::register($script_name,$script_version,$script_description,\&unload);


# Let the user know the plugin has been loaded.


Xchat::print("Loaded \002".$script_name."\002:");

Xchat::print("Use \002/mhelp\002 to display a list of commands.");



# Register the commands.



Xchat::hook_command("mhelp",\&mhelp);

Xchat::hook_command("media",\&media);

Xchat::hook_command("next",\&next);

Xchat::hook_command("prev",\&prev);

Xchat::hook_command("play",\&play);

Xchat::hook_command("pause",\&pause);

Xchat::hook_command("rate",\&rate);



## HELP 



sub mhelp

{

# Display help screen.

Xchat::print("\002\037".$script_name." Help:\037\002");

Xchat::print(" \002About:\002");

Xchat::print(" * Author: Will Farrington [www.kalmwave.com] <wcfarrington@gmail.com>");

Xchat::print(" * Script Version: ".$script_version);

Xchat::print(" * XChat Version: ".Xchat::get_info(0));

Xchat::print(" \002Commands:\002");

Xchat::print(" * /mhelp - Display this screen.");

Xchat::print(" * /media - Display the current song playing to a channel.");

Xchat::print(" * /next - Skips to next song.");

Xchat::print(" * /prev - Skips to previous song.");

Xchat::print(" * /play - Starts playback.");

Xchat::print(" * /pause - Pauses playback.");

Xchat::print(" * /rate - Allows rating of currently playing song.");

}



# Grab the current Banshee version.



$banshee_version = `banshee --version`;

chop $banshee_version;


# Declare these variables now so that when we run the subroutine grab_song, it works like we want.

my ($artist, $track, $pos, $dur, $true_pos, $true_dur, $rating, $maxrating, $album, $rating2, $obj, $iface);
 

## TEST DBUS



sub test_dbus

{

	my $service = shift;

 

	my $bus = Net::DBus->session;

	my $obj = $bus->get_service("org.freedesktop.DBus");

	my $iface = $obj->get_object("/org/freedesktop/DBus", 

		"org.freedesktop.DBus");

 

	foreach my $item( @{$iface->ListNames()} )

	{

		if( $item eq $service )

		{

			return 1;

		}

	}

 

	return 0;

}



# Set DBUS vars for Banshee.



my($data, $server, $witem) = @_;

 

my $bus = Net::DBus->session;

 
## ESTABLISH IF BANSHEE IS RUNNING IN DBUS


sub dbus_stuff {
if(!&test_dbus("org.gnome.Banshee"))

{

	Xchat::print("Could not see Banshee in dbus.");
	return Xchat::EAT_PLUGIN;

}

# Set Banshee's "address" for DBUS.


$obj = $bus->get_service("org.gnome.Banshee");

$iface = $obj->get_object("/org/gnome/Banshee/Player",

		"org.gnome.Banshee.Core");
}



## GRAB SONG INFORMATION



sub grab_song

{
dbus_stuff();


# Get current playing song information.

$artist = $iface->GetPlayingArtist;

$track = $iface->GetPlayingTitle;

$album = $iface->GetPlayingAlbum;

$true_pos = $iface->GetPlayingPosition;

$true_dur = $iface->GetPlayingDuration;

$rating = $iface->GetPlayingRating;

$maxrating = $iface->GetMaxRating;

# If the song hasn't been rated, show "Not Rated" instead of "0/5".



if ($rating == 0) {

$rating2 = "Not Rated.";

} else {

$rating2 = $rating;

}


# Fix for Banshee duration and position.

chop $pos;

chop $dur;

$pos = sprintf("%d:%02d", int($true_pos / 60), $true_pos % 60);

$dur = sprintf("%d:%02d", int($true_dur / 60), $true_dur % 60);



return 0;

}



## PRINT PLAYING MEDIA



sub media

{

grab_song();


# Say the current playing song in the channel.


# If the song has no rating yet, show "Not Rated" instead.
	if ($rating == 0) {
		

Xchat::command("me is listening to 12$track01 by 13$artist01 on 10$album01 using $banshee_version Rated: $rating2 ($pos/$dur)");



} else { 



Xchat::command("me is listening to 12$track01 by 13$artist01 on 10$album01 using $banshee_version Rated: $rating2"."/"."$maxrating ($pos/$dur)"); 



}

return 1;

}


## SKIP TRACK


sub next

{
dbus_stuff();


# Skip to the next track.

$iface->Next;


# Echo in the window what we just did.
Xchat::print("Skipped to next track.");

return 1;

}


## SKIP TO LAST TRACK


sub prev

{
dbus_stuff();


# Skip to the previous track.

$iface->Previous;


# Echo in the window what we just did.
Xchat::print("Skipped to previous track.");

return 1;

}


## PLAY MEDIA


sub play

{
dbus_stuff();


# Start playback.

$iface->Play;


# Echo in the window what we just did.
Xchat::print("Started playback.");

return 1;

}



## PAUSE MEDIA


sub pause

{
dbus_stuff();


# Pause playback.

$iface->Pause;

# Echo in the window what we just did.

Xchat::print("Paused playback.");

return 1;

}


## RATE MEDIA


sub rate {

grab_song();
use Net::DBus qw(:typing);


# Rate the song. Notice the use of dbus_int32 to get a dbus-compliant integer as the result.
$newrating = dbus_int32($_[0][1]);

$iface->SetPlayingRating($newrating);

# Echo in the window what we just did.

Xchat::print("Rated $track by $artist a $_[0][1]/$maxrating.");

return 1;

}

