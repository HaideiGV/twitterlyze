import logging
from datetime import datetime
from typing import Dict

from db.base import posts_analytic

log = logging.getLogger(__name__)


async def add_posts_analytic(db, data: Dict):

    async with db.acquire() as conn:
        try:
            log.info("Start writing analytic...")
            await conn.execute(
                posts_analytic
                .insert()
                .values(
                    executed_at=datetime.now(),
                    interval=data['search_interval'],
                    search_phrase=data['search_phrase'],
                    top_hashtags=data['top_hashtags'],
                    top_phrases=data['top_phrases'],
                    top_publisher=data['top_publisher'],
                    tweet_count=data['tweet_count']
                )
            )
            log.info("Writing analytic finished.")
        except Exception as e:
            log.error(
                "Adding to database was failed due to: {}".format(str(e))
            )


async def get_posts_analytic(db):
    result = []
    async with db.acquire() as conn:
        data = await conn.execute(posts_analytic.select())
        async for row in data:
            result.append(row)

    return result


async def get_posts_analytic_by_phrase(db, phrase):
    result = []
    async with db.acquire() as conn:
        data = await conn.execute(
            posts_analytic
            .select()
            .where(posts_analytic.c.search_phrase == phrase)
        )
        async for row in data:
            result.append(row)

    return result
