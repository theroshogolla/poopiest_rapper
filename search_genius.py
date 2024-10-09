import os
import lyricsgenius as genius
import requests
import urllib.parse
import json

def setup_credentials() -> dict:
        with open('credentials', 'r') as creds:
                for line in creds.readlines():
                        assign = line.split('=')
                        
                        os.environ[assign[0]] = assign[1].strip('\n')

        headers = {'Authorization': f'bearer {os.environ["CLIENT_ACCESS_TOKEN"]}'}
        return headers

URL = 'https://genius.com/api'
headers = setup_credentials()

params = { 'q': 'Rakim'}

res = requests.get(f'{URL}/search/multi', params=params)

with open('response_song', 'w') as f:
    f.write(json.dumps(res.json()))


# api = genius.Genius()

# jid = api.search_artist('JID', max_songs=50)