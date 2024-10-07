import os
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

URL = 'https://api.genius.com'
headers = setup_credentials()

res = requests.get(f'{URL}/search?q={urllib.parse.quote("Dr. Dre")}', headers=headers)

with open('response_song', 'w') as f:
    f.write(json.dumps(res.json()))