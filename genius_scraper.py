import os
import requests
import urllib.parse
import json

with open('credentials', 'r') as creds:
        for line in creds.readlines():
            assign = line.split('=')
            
            os.environ[assign[0]] = assign[1].strip('\n')

headers = {'Authorization': f'bearer {os.environ["CLIENT_ACCESS_TOKEN"]}'}

URL = 'https://api.genius.com/'
query = 'Kendrick Lamar'

res = requests.get(f'{URL}search?q={urllib.parse.quote(query)}', headers=headers)

results = res.json()['response']['hits']

# for item in results:
#     print(f'Song title: {item["result"]["title"]} | Song ID: {item["result"]["id"]} | Artist Name: {item["result"]["primary_artist"]["name"]} | Artist ID: {item["result"]["primary_artist"]["id"]}')

artist_path = results[0]['result']['primary_artist']['api_path']

for i in range(1, 4):
    params = {'sort': 'popularity',
            'per_page': 50,
            'page': i}

    res = requests.get(f'{URL}{artist_path}/songs/', params=params, headers=headers)

    results = res.json()['response']['songs']
