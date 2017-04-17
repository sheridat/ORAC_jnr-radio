#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
import sys
import time

from mpd import (MPDClient, CommandError)
from socket import error as SocketError

HOST = 'localhost'
PORT = '6600'
PASSWORD = False
##
CON_ID = {'host':HOST, 'port':PORT}
##  

## Some functions
def mpdConnect(client, con_id):
    """
    Simple wrapper to connect MPD.
    """
    try:
        client.connect(**con_id)
    except SocketError:
        return False
    return True

def mpdAuth(client, secret):
    """
    Authenticate
    """
    try:
        client.password(secret)
    except CommandError:
        return False
    return True
##

def main():
    ## MPD object instance
    client = MPDClient()
    if mpdConnect(client, CON_ID):
        print('Got connected!')
    else:
        print('fail to connect MPD server.')
        sys.exit(1)

    # Auth if password is set non False
    if PASSWORD:
        if mpdAuth(client, PASSWORD):
            print('Pass auth!')
        else:
            print('Error trying to pass auth.')
            client.disconnect()
            sys.exit(2)

    while(1):

        client.send_idle()
        state = client.fetch_idle()

        if (state[0] == 'mixer'):
            print('Volume = ' + client.status()['volume'])

        if (state[0] == 'player'):
            try:
                station = client.currentsong()['name']
            except KeyError:
                station = ''
 
            try:
                title = client.currentsong()['title']
            except KeyError:
                title = ''

            try:
                artist = client.currentsong()['artist']
            except KeyError:
                artist = ''

            if(station != ''):    # webradio
                print('Station = ' + station)
                print('Title = ' + title)
            else:                 # file
                print('Title = ' + title)
                print('Artist = ' + artist)

        if (state[0] == 'playlist'):
            print('the current playlist has been modified')

        if (state[0] == 'database'): 
           print('the song database has been modified after update')

        if (state[0] == 'update'): 
           print('a database update has started or finished. If the database was modified during the update, the database event is also emitted.')

        if (state[0] == 'stored_playlist'): 
           print('a stored playlist has been modified, renamed, created or deleted')

        if (state[0] == 'output'): 
           print('an audio output has been enabled or disabled')

        if (state[0] == 'options'): 
           print('options like repeat, random, crossfade, replay gain')

        if (state[0] == 'sticker'): 
           print('the sticker database has been modified.')

    ## disconnect
    client.disconnect()
    sys.exit(0)

# Script starts here
if __name__ == "__main__":
    main()
