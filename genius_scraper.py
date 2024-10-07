import os
import requests
import urllib.parse
import json
from typing import Literal

def is_relevant_artist(song: dict, artist: str) -> bool:
        primary_names =[pa['name'].lower() for pa in song['primary_artists']]
        featured_names = [fa['name'].lower() for fa in song['featured_artists']]
        artist_names = [*primary_names, *featured_names]
        print(artist_names)
        for name in artist_names:
                if artist.lower() == name or artist.lower() in name:
                        return True
        return False

def setup_credentials() -> dict:
        with open('credentials', 'r') as creds:
                for line in creds.readlines():
                        assign = line.split('=')
                        
                        os.environ[assign[0]] = assign[1].strip('\n')

        headers = {'Authorization': f'bearer {os.environ["CLIENT_ACCESS_TOKEN"]}'}
        return headers

URL = 'https://api.genius.com'
headers = setup_credentials()
rappers = []
with open('rappers.txt', 'r') as rappers_file:
        rappers = rappers_file.readlines()

for rapper in rappers:
        rapper = rapper.strip('\n')
        res = requests.get(f'{URL}/search?q={urllib.parse.quote(rapper)}', headers=headers)

        results = res.json()['response']['hits']
        artist_id = results[0]['result']['primary_artist']['id']
        artist_path = results[0]['result']['primary_artist']['api_path']

        with open('data/artist_ids.csv', 'a') as ids:
                ids.write(f'{artist_id}, {rapper}\n')
# for item in results:
#     print(f'Song title: {item["result"]["title"]} | Song ID: {item["result"]["id"]} | Artist Name: {item["result"]["primary_artist"]["name"]} | Artist ID: {item["result"]["primary_artist"]["id"]}')

        for i in range(1, 4):
                params = { 'sort': 'popularity',
                         'per_page': 50,
                         'page': i}

                res = requests.get(f'{URL}{artist_path}/songs/', params=params, headers=headers)

                songs = res.json()['response']['songs']
                rapper_filename = rapper.replace(' ', '_')
                for song in songs:
                        print(f'{song["title"]} | {song["primary_artist"]["name"]} | {is_relevant_artist(song, rapper)}')
                        if not is_relevant_artist(song, rapper):
                                continue
                        else:
                                if not os.path.exists(f'data/{artist_id}.csv'):
                                        with open(f'data/{artist_id}.csv', 'w') as f:
                                                f.write('id,title,url,artist_id\n')
                                                f.write(f'{song["id"]},{song["title"]},{song["url"]},{artist_id}\n')
                                else:
                                        with open(f'data/{artist_id}.csv', 'a') as f:
                                                f.write(f'{song["id"]},{song["title"]},{song["url"]},{artist_id}\n')



