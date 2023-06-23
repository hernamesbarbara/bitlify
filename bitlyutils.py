#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import os
import pandas as pd

with open(os.path.expanduser('~/.bitly'), 'r') as f:
    ACCESS_TOKEN = f.read().strip()

def shorten_url(url, title):
    endpoint = 'https://api-ssl.bitly.com/v4/shorten' 

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    } 

    data = {
        "title": title,
        "long_url": url
    }

    r = requests.post(endpoint, headers=headers, data=json.dumps(data)) 
    
    if r.status_code == 200:
        short_url = json.loads(r.content)['link']
        data['short_url'] = short_url
        return data
    else:
        print('something went wrong')
        print(json.dumps(json.loads(r.content), indent=2))
        return data


df = pd.read_csv(os.path.expanduser('~/Desktop/urls.csv'))

df.columns = [col.lower() for col in df.columns]

row = df.head(1).to_dict(orient='records')[0]

r = shorten_url(row['url'], row['title'])

# print(json.dumps(json.loads(df.to_json(orient='records')), indent=2))

results = []

docs = df.to_dict(orient='records')

for i, doc in enumerate(docs):
    print(f"{i+1} of {len(df)}")
    print(doc.get('title'))
    if doc.get('url'):
        print(doc['url'])
        print()
    else:
        print('Missing URL...skipping')
        print()
        continue
    res = shorten_url(doc['url'], doc['title'])
    results.append(res)


df_out = pd.DataFrame(results)

df_out.to_csv('output.csv', index=False, encoding='utf-8')

print('done and done')