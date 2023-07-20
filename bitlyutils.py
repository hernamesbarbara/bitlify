#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""bitlyutils.py

Usage:
  bitlyutils.py <url_file>

Arguments:
  url_file     The CSV file containing URLs to be shortened.
  
Options:
  -h --help    Show this screen.

"""

import requests
import json
import os
import string
import pandas as pd
from docopt import docopt

# Reading Bitly access token from the file
with open(os.path.expanduser('~/.bitly'), 'r') as f:
    ACCESS_TOKEN = f.read().strip()

# Function to shorten URL using Bitly API
def shorten_url(url, title):
    """Shorten a given URL using Bitly API.
    
    Args:
        url (str): The original URL to be shortened.
        title (str): The title associated with the URL.

    Returns:
        r (Response object): The server's response to the request.
    """
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
    return r
    
# Function to customize back-half of a short URL using Bitly API
def customize_short_url_back_half(bitlink_id, custom_bitlink):
    """Customize back-half of a short URL using Bitly API.

    Args:
        bitlink_id (str): The bitlink ID to be customized.
        custom_bitlink (str): The desired custom back-half for the short URL.

    Returns:
        r (Response object): The server's response to the request.
    """
    endpoint = 'https://api-ssl.bitly.com/v4/custom_bitlinks'
    
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    } 
    
    data = {
        "custom_bitlink": custom_bitlink,
        "bitlink_id": bitlink_id
    }
    
    r = requests.post(endpoint, headers=headers, data=json.dumps(data))
    
    return r


def main(args):
    df = pd.read_csv(args['<url_file>'])
    df.columns = [col.lower() for col in df.columns]
    results = []
    docs = df.to_dict(orient='records')

    for i, doc in enumerate(docs):
        res = {}
        print(f"{i+1} of {len(df)}")
        res = shorten_url(doc['url'], doc['title'])
        data = res.json()
        if data.get('id'):
            domain = data['id'].split('/')[0]
            if doc.get('backhalf'):
                res_custom_short_url = customize_short_url_back_half(data['id'], domain+'/'+doc['backhalf'])
                if res_custom_short_url and res_custom_short_url.status_code == 200:
                    if res_custom_short_url.json().get('custom_bitlink'):
                        data['short_url'] = res_custom_short_url.json()['custom_bitlink']
            else:
                data['short_url'] = data['link']
        print(f"{doc.get('title')} => {data['short_url']}")
        results.append(data)

    df_out = pd.DataFrame(results)
    df_out.to_csv('output.csv', index=False, encoding='utf-8')

    print()
    print('done and done')
    print('*'*40+'\n')

if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(arguments)