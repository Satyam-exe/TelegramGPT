import tempfile

from .config import ytmusic_client, get_ytmusic_song_url

from yt_dlp import YoutubeDL

from settings import TEMP_OGG_DIR


def get_music_results(query, query_type):
    search_results = ytmusic_client.search(query=query, filter=query_type, limit=1)
    return search_results


def convert_yt_to_ogg(song_id):
    music_url = get_ytmusic_song_url(song_id)
    temp_dir = tempfile.TemporaryDirectory(dir=TEMP_OGG_DIR)
    options = {
        'format': 'bestaudio',
        'outtmpl': f'{temp_dir.name}/%(title)s.ogg'
    }
    with  YoutubeDL(options) as ytdl:
        ytdl.download([music_url])
    return temp_dir
