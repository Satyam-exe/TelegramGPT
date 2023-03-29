from ytmusicapi import YTMusic

query_types = [
    'songs',
]

ytmusic_client = YTMusic()

get_ytmusic_song_url = lambda id: f'https://music.youtube.com/watch?v={id}'
