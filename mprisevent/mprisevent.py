#!/usr/bin/env python3
import argparse
import datetime
from functools import partial

import requests

from dbus.mainloop.glib import DBusGMainLoop
from mpris2 import Player, get_players_uri

import gi.repository.GLib


def properties_changed(url, auth, *args, **kwargs):
    if 'Metadata' in args[1]:
        md = args[1]['Metadata']
        if 'xesam:url' in md:
            if 'xesam:contentCreated' in md:
                try:
                    year = ' ' + md.get('xesam:contentCreated')[:4] + ' '
                except KeyError:
                    year = ' '
            else:
                year = ' '
            try:
                track = md.get('xesam:title')
            except KeyError:
                track = ' ' 
            if 'xesam:artist':
                try:
                    artist = ', '.join(md.get('xesam:artist', ['Unknown Artist']))
                except KeyError:
                    artist = ' ' 
            else:
                artist = ' ' 
            if 'xesam:album':
                try:
                    album = md.get('xesam:album', 'Unknown Album')
                except KeyError:
                    album = ' ' 
            else:
                album = ' '
            if 'xesam:comment':
                if md.get('xesam:comment'):
                    try:
                        comment = md.get('xesam:comment')[0].replace('・', '- ')
                    except KeyError:
                        comment = ' ' 
                else: comment = ' '
            else: comment = ' '
            if comment is not ' ':
                comment = " -- " + comment
            now_playing = '"{track}" by {artist}, on their{year}album "{album}" {comment}'.format(
                track = track, 
                artist = artist, 
                year = year,
                album = album, 
                comment = comment 
            )
            print(now_playing)
            params = (('mount', '/Music'), ('mode', 'updinfo'), ('song', now_playing),)
            try:
                requests.get(url, params=params, auth=auth, timeout=1)
            except (requests.exceptions.RequestException, ConnectionResetError) as err:
                print('An error happened and was ignored:')
                print(err)
                print('Will try to update again at next song change.')


def main():
    parser = argparse.ArgumentParser(description='MPRIS to Icecast bridge.')
    parser.add_argument('url', type=str, help='URL to Icecast server.')
    parser.add_argument('username', type=str, help='Username')
    parser.add_argument('password', type=str, help='Password')

    args = parser.parse_args()

    DBusGMainLoop(set_as_default=True)

    uri = next(get_players_uri())
    player = Player(dbus_interface_info={'dbus_uri': uri})

    player.PropertiesChanged = partial(properties_changed, args.url, (args.username, args.password))

    mloop = gi.repository.GLib.MainLoop()
    mloop.run()

if __name__ == '__main__': main()
