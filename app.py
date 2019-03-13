import asyncio
from aiohttp import web
from aiohttp.abc import AbstractAccessLogger

from handlers.health import health_handler
from handlers.index import index_handler
from handlers.search_settings import get_search_settings, post_search_settings
from handlers.search_results import (
    get_search_results, get_search_results_by_phrase,
)
from db.base import init_pg
from job import parse_activity


class AccessLogger(AbstractAccessLogger):

    def log(self, request, response, time):
        self.logger.info(
            f'[{request.remote}][{request.method}] '
            f'{request.path} done in {time}s: {response.status}'
        )


async def create_tables(app):
    async with app['db'].acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS public.posts_analytic (
                id serial PRIMARY KEY NOT NULL,
                executed_at timestamp,
                interval integer,
                search_phrase varchar(256),
                top_hashtags text[],
                top_phrases text[],
                top_publisher bigint,
                tweet_count integer
            );
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS public.search_settings (
                id serial PRIMARY KEY NOT NULL,
                search_phrase varchar(256),
                search_interval integer
            );
        """)


async def on_startup(app):
    await init_pg(app)
    await create_tables(app)
    app['tasks'].append(app.loop.create_task(parse_activity(app)))


async def on_shutdown(app):
    await app['db'].close()
    for task in app['tasks']:
        await task.close()


loop = asyncio.get_event_loop()
app = web.Application(loop=loop)
app['tasks'] = []

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
app.add_routes([
    web.get('/health', health_handler),
    web.get('/search_settings/', get_search_settings),
    web.post('/search_settings/', post_search_settings),
    web.get('/search_results/', get_search_results),
    web.get('/search_results/{phrase}/', get_search_results_by_phrase),
    web.get('/', index_handler)
])

web.run_app(app, access_log_class=AccessLogger)
