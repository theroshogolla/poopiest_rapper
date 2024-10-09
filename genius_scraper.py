import os
import requests
import urllib.parse
import json
import html
from tqdm import tqdm
import pandas as pd

URL = 'https://api.genius.com'
PUBLIC_URL = 'https://genius.com/api'

def is_relevant_artist(song: dict, artist: str) -> bool:
        primary_names =[html.unescape(pa['name']).lower() for pa in song['primary_artists']]
        featured_names = [html.unescape(fa['name']).lower() for fa in song['featured_artists']]
        artist_names = [*primary_names, *featured_names]
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

def get_artist_id(artist_name: str) -> int:
        params = {'q': artist_name}
        res = requests.get(f'{PUBLIC_URL}/search/multi', params=params)
        #print(res.status_code)
        res_sections = res.json()['response']['sections']
        for section in res_sections:
                for hit in section['hits']:
                        if not (hit['type'] == 'artist' or hit['type'] == 'user'):
                                continue
                        else:
                                print(html.unescape(hit['result']['name']).lower())
                                print(artist_name.lower())
                                if html.unescape(hit['result']['name']).lower() == artist_name.lower():
                                        return hit['result']['id']
        return -1

def get_artist_songs(artist_id: int):
        headers = setup_credentials()
        params = {'sort': 'popularity',
                  'per_page': 50,
                  'page': 1}
        res = requests.get(f'{URL}/artists/{artist_id}/songs', params=params, headers=headers)
        print(res.json())
        response = res.json()['response']
        process_songs(response, artist_id)
        while response['next_page']:
                params['page'] = response['next_page']
                res = requests.get(f'{URL}/artists/{artist_id}/songs', params=params, headers=headers)
                response = res.json()['response']
                process_songs(response, artist_id)

def process_songs(api_response: dict, artist_id: int):
        songs = api_response['songs']
        for song in songs:
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

rappers = []
with open('rappers.txt', 'r', encoding="utf-8") as rappers_file:
        rappers = rappers_file.readlines()

processed_rappers = [name.strip(' ') for name in (pd.read_csv(os.path.join('data', 'artist_ids.csv'), escapechar='\\'))['name'].values]
#print(processed_df['name'].values)

for rapper in tqdm(rappers):
        rapper = rapper.strip('\n')
        if rapper in processed_rappers:
                print(f'Skipping {rapper}')
                continue
        artist_id = get_artist_id(rapper)
        if artist_id == -1:
                raise ValueError(f'Could not find ID for artist {rapper}')
        
        with open('data/artist_ids.csv', 'a') as ids:
                ids.write(f'{artist_id}, {rapper}\n')
        get_artist_songs(artist_id)
# for item in results:
#     print(f'Song title: {item["result"]["title"]} | Song ID: {item["result"]["id"]} | Artist Name: {item["result"]["primary_artist"]["name"]} | Artist ID: {item["result"]["primary_artist"]["id"]}')