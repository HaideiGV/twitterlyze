import trafaret as t
from trafaret import DataError
from aiohttp import web

from db.search_settings import get_setting, add_or_update_setting


search_settings_schema = t.Dict({
    t.Key('search_phrase') >> 'search_phrase': t.String,
    t.Key('search_interval') >> 'search_interval': t.Int
})


async def get_search_settings(request):
    db = request.app['db']
    data = await get_setting(db)
    return web.json_response(data=data, content_type='application/json')


async def post_search_settings(request):
    db = request.app['db']
    data = await request.json()

    try:
        validated = search_settings_schema.check(data)
    except DataError as err:
        return web.HTTPError(reason=err.error)

    await add_or_update_setting(db, validated)

    updated_data = await get_setting(db)

    return web.json_response(
        data=updated_data, content_type='application/json'
    )
