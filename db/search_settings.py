from typing import Dict, Optional

from db.base import search_settings


async def get_setting(db) -> Optional[Dict]:
    phrase = ''
    interval = 0
    async with db.acquire() as conn:
        result = await conn.execute(search_settings.select().limit(1))
        async for row in result:
            interval, phrase = row[2], row[1]

    return {'search_phrase': phrase, 'search_interval': interval}


async def add_or_update_setting(db, data: Dict):
    phrase = data['search_phrase']
    interval = data['search_interval']
    setting = await get_setting(db)

    if setting:
        query = (
            search_settings
            .update()
            .where(search_settings.c.id == 1)
            .values(search_phrase=phrase, search_interval=interval)
        )
    else:
        query = (
            search_settings
            .insert()
            .values(search_phrase=phrase,search_interval=interval)
        )

    async with db.acquire() as conn:
        await conn.execute(query)
