import os
from typing import List, Dict

import requests

TWITTER_GENERATED_TOKEN = os.environ.get(
    'TWITTER_GENERATED_TOKEN',
    f'AAAAAAAAAAAAAAAAAAAAAIZB9gAAAAAAgN6r7Bb3pyoOdF%2F3s0y'
    f'TWAAFGTw%3DjAPs2TjNFZsSvmKMzulTGsCnSqaC5Zs0g6ROE0V3Eg2YoaKPB7'
)


def get_posts(search_string: str, count: int) -> List[Dict]:
    tweets_data_request = requests.get(
        url='https://api.twitter.com/1.1/search/tweets.json',
        headers={'Authorization': f'Bearer {TWITTER_GENERATED_TOKEN}'},
        params={'q': search_string, 'count': count},
    )

    return tweets_data_request.json().get('statuses', [])
