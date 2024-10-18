import os
import requests
import urllib.parse
import json
import html
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
import random

SEED = 34567

random.seed(SEED)

song_meta_file = []

metadata_files = os.listdir('data')
metadata_files.remove('artist_ids_backup.csv')
metadata_files.remove('artist_ids.csv')

meta_filename = metadata_files[random.randint(0, (len(metadata_files) - 1))]

with open(os.path.join('data', meta_filename), 'r') as f:
    song_meta_file = f.readlines()[1:]

test_song = song_meta_file[random.randint(0, (len(metadata_files) - 1))]

song_info = test_song.split(',')

res = requests.get(song_info[2])

soup = BeautifulSoup(res.text, 'html.parser')

lyrics_tags = soup.find_all(lambda tag: (tag.name == 'div') and (tag.has_attr('data-lyrics-container')) and (tag['data-lyrics-container'] == 'true'))

lyrics = []
for div in lyrics_tags:
    lyrics.extend(div.stripped_strings)

print(f'SONG NAME: {song_info[1]}')
print(lyrics)