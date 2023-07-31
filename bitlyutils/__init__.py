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