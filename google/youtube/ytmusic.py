import os
import tempfile

from pydub import AudioSegment

from .config import ytmusic_client, get_ytmusic_song_url
from pytube import YouTube

from settings import TEMP_OGG_DIR


def get_music_results(query, type):
    search_results = ytmusic_client.search(query=query, filter=type, limit=1)
    return search_results


def convert_yt_to_ogg(song_id):
    music_url = get_ytmusic_song_url(song_id)
    pytube_client = YouTube(url=music_url)
    video = pytube_client.streams.filter(only_audio=True).first()
    temp_dir = tempfile.TemporaryDirectory(dir=TEMP_OGG_DIR)
    mp4_file = video.download(output_path=temp_dir.name)
    base, extension = os.path.splitext(mp4_file)
    ogg_file = base + '.ogg'
    os.rename(mp4_file, ogg_file)
    return [ogg_file, temp_dir]

