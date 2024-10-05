import os
import requests
import urllib.parse
import json

with open('credentials', 'r') as creds:
        for line in creds.readlines():
            assign = line.split('=')
            
            os.environ[assign[0]] = assign[1].strip('\n')

headers = {'Authorization': f'bearer {os.environ["CLIENT_ACCESS_TOKEN"]}'}

URL = 'https://api.genius.com/search?q='
query = 'Kendrick Lamar'

res = requests.get(f'{URL}{urllib.parse.quote(query)}', headers=headers)

with open('response', 'w+') as res_txt:
    res_txt.write(json.dumps(res.json()))
