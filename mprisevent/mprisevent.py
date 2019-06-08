import argparse
import datetime
from functools import partial

import requests

from dbus.mainloop.glib import DBusGMainLoop
from mpris2 import Player, get_players_uri

import gi.repository.GLib


def properties_changed(url, auth, *args, **kwargs):
    if 'Metadata' in args[1]:
        md = dict(args[1]['Metadata'])
        if 'xesam:url' in md:
            try:
                year = ' ' + md.get('xesam:contentCreated')[:4] + ' '
            except KeyError:
                year = ' '

            now_playing = '"{track}" by {artist}, on their{year}album "{album}"'.format(
                track = md.get('xesam:title', 'Unknown Track'),
                artist = ', '.join(md.get('xesam:artist', ['Unknown Artist'])),
                year = year,
                album = md.get('xesam:album', 'Unknown Album')
            )
            print(now_playing)
            params = (('mount', '/Music'), ('mode', 'updinfo'), ('song', now_playing),)
            requests.get(url, params=params, auth=auth, timeout=1)


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
