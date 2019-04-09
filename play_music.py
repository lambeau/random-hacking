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

    def do_dump_artist(self, query):
        seed_song = search(self.api, query)
        artist_id = seed_song['artist_id']
        title = seed_song['artist']
        station_id = self.api.create_station('temp station', artist_id=artist_id)
        self.dump(station_id, title)

    def do_dump_song(self, query):
        seed_song = search(self.api, query)
        track_id = seed_song['store_id']
        title = seed_song['title']
        station_id = self.api.create_station('temp station', track_id=track_id)
        self.dump(station_id, title)

    def dump(self, station_id, title):
        """Dump a station based on query to a playlist"""
        track_ids = []
        count = 0
        while len(track_ids) < 1000 and count < 20:
            tracks = self.api.get_station_tracks(station_id, num_tracks=1000, recently_played_ids=track_ids)
            track_ids += [track['storeId'] if 'storeId' in track else track['id'] for track in tracks]
            count += 1
            print('{} - {}'.format(count, len(track_ids)))
        print('creating playlist')
        playlist_id = self.api.create_playlist(
            'g {} {}'.format(title, datetime.now().isoformat(' ')))
        print('adding songs')
        self.api.add_songs_to_playlist(playlist_id, list(set(track_ids)))  # duplicates are possible for uploaded songs
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
    artist_id = raw['track']['artistId'][0]
    return {'title': title,
            'artist': artist,
            'album': album,
            'store_id': store_id,
            'artist_id': artist_id}


if __name__ == '__main__':
    Shell().cmdloop()
