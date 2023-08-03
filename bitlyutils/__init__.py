#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bitlyutils/__init__.py
"""
import requests
import json

def shorten_url(url, title, access_token):
    """Shorten a given URL using Bitly API.
    
    Args:
        url (str): The original URL to be shortened.
        title (str): The title associated with the URL.

    Returns:
        r (Response object): The server's response to the request.
    """
    endpoint = 'https://api-ssl.bitly.com/v4/shorten' 

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    } 

    data = {
        "title": title,
        "long_url": url
    }

    r = requests.post(endpoint, headers=headers, data=json.dumps(data)) 
    return r
    

def customize_short_url_back_half(bitlink_id, custom_bitlink, access_token):
    """Customize back-half of a short URL using Bitly API.

    Args:
        bitlink_id (str): The bitlink ID to be customized.
        custom_bitlink (str): The desired custom back-half for the short URL.

    Returns:
        r (Response object): The server's response to the request.
    """
    endpoint = 'https://api-ssl.bitly.com/v4/custom_bitlinks'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    } 
    
    data = {
        "custom_bitlink": custom_bitlink,
        "bitlink_id": bitlink_id
    }
    
    r = requests.post(endpoint, headers=headers, data=json.dumps(data))
    
    return r

def process_single_url(url, access_token, title=None, backhalf=None):
    """Process a single URL and return the result as a dictionary.

    Args:
        url (str): The original URL to be shortened.
        access_token (str): The Bitly access token.
        title (str, optional): The title associated with the URL. Default is None.
        backhalf (str, optional): Desired custom back-half for the short URL. Default is None.

    Returns:
        data (dict): The resulting data from the Bitly API calls.
    """
    if title:
        res = shorten_url(url, title, access_token)
    else:
        res = shorten_url(url, '', access_token)
    
    data = res.json()
    if data.get('id'):
        domain = data['id'].split('/')[0]
        if backhalf:
            res_custom_short_url = customize_short_url_back_half(data['id'], domain+'/'+str(backhalf), access_token)
            if res_custom_short_url and res_custom_short_url.status_code == 200:
                if res_custom_short_url.json().get('custom_bitlink'):
                    data['short_url'] = res_custom_short_url.json()['custom_bitlink']
        else:
            data['short_url'] = data['link']
    return data

def process_url_list(url_list, access_token):
    """Process a list of URLs and return the results as a list of dictionaries.

    Args:
        url_list (list of dict): A list of dictionaries each containing 'url', 'title' and 'backhalf' keys.
        access_token (str): The Bitly access token.

    Returns:
        results (list of dict): A list of resulting data from the Bitly API calls.
    """
    results = []
    for i, url_info in enumerate(url_list):
        url = url_info['url']
        title = url_info.get('title') 
        backhalf = url_info.get('backhalf')
        # print(f"{i+1} of {len(url_list)}")
        result = process_single_url(url, access_token, title, backhalf)
        # print(f"{url} => {result['short_url']}")
        results.append(result)
    return results