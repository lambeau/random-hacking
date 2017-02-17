import getpass
import json
from datetime import datetime
import cmd

import gmusicapi  # https://github.com/simon-weber/gmusicapi


class Shell(cmd.Cmd):
    intro = 'Play music interactive shell. Login required.\nType help or ? to list commands.'
    prompt = '(gpm) '
    api = None
    use_rawinput = False

    def do_search(self, query):
        """Search for a song"""
        print(json.dumps(search(self.api, query), indent=2))

    def do_login(self, username):
        """Login to Google Play Music: LOGIN <username>"""
        if self.api is None:
            api = gmusicapi.Mobileclient()
            password = getpass.getpass()
            logged_in = api.login(username, password, gmusicapi.Mobileclient.FROM_MAC_ADDRESS)
            if logged_in:
                self.api = api
                print('logged in')
            else:
                print('login failed')
        else:
            print('already logged in')

    def do_dump(self, query):
        """Dump a station based on query to a playlist"""
        seed_song = search(self.api, query)
        station_id = self.api.create_station('temp station', track_id=seed_song['store_id'])
        track_ids = []
        count = 0
        while len(track_ids) < 1000 and count < 10:  # Seems to stop at 200 tracks regardless of count
            tracks = self.api.get_station_tracks(station_id, num_tracks=1000, recently_played_ids=track_ids)
            track_ids += [track['storeId'] for track in tracks]
            count += 1
            print('{} - {}'.format(count, len(track_ids)))
        print('creating playlist')
        playlist_id = self.api.create_playlist(
            'g {} {}'.format(seed_song['title'], datetime.now().isoformat(' ')))
        print('adding songs')
        self.api.add_songs_to_playlist(playlist_id, track_ids)
        print('songs added')

    def do_exit(self, arg):
        """Exit"""
        return True


def search(api, query):
    results = api.search(query)
    raw_song = results.get('song_hits', [None])[0]
    result = get_song_info(raw_song)
    return result


def get_song_info(raw):
    title = raw['track']['title']
    artist = raw['track']['artist']
    album = raw['track']['album']
    store_id = raw['track']['storeId']
    return {'title': title,
            'artist': artist,
            'album': album,
            'store_id': store_id}


if __name__ == '__main__':
    Shell().cmdloop()
