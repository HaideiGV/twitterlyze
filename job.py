import asyncio
from typing import List, Dict
from collections import Counter

from db.posts import add_posts_analytic
from db.search_settings import get_setting
from twapi import get_posts

POSTS_COUNT = 100


def get_data(search_phrase: str) -> List[Dict]:
    return get_posts(search_phrase, POSTS_COUNT)


def analyse_data(data: List[Dict]):
    tweet_count = len(data)
    hashtags = Counter()
    publishers = Counter()
    phrases = Counter()
    for entity in data:
        user_id = entity['user']['id']
        publishers[user_id] += 1

        for tag in entity['entities']:
            hashtags[tag] += 1

        post_words = entity['text'].split(' ')
        bi_grams = tuple(zip(post_words, post_words[1:]))
        for bi_gram in bi_grams:
            phrases[bi_gram] += 1

    top_phrases = [
        " ".join([phrase[0], phrase[1]])
        for phrase, _ in phrases.most_common(3)
    ]
    return {
        'top_hashtags': [tag for tag, _ in hashtags.most_common(3)],
        'top_phrases': top_phrases,
        'top_publisher': publishers.most_common(1)[0][0],
        'tweet_count': tweet_count
    }


async def parse_activity(app):
    db = app['db']

    setting = await get_setting(db)
    data = get_data(setting['search_phrase'])
    statistic = analyse_data(data)
    setting.update(statistic)

    await add_posts_analytic(db, setting)

    await asyncio.sleep(int(setting['search_interval']))

    await parse_activity(app)
