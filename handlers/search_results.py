import base64
import binascii

from aiohttp import web

from db.posts import get_posts_analytic, get_posts_analytic_by_phrase
from handlers.helper import gen_analytic_result


async def get_search_results(request):
    db = request.app['db']
    posts_analytic = await get_posts_analytic(db)
    results = gen_analytic_result(posts_analytic)

    return web.json_response(
        data={"search_results": results},
        content_type='application/json'
    )


async def get_search_results_by_phrase(request):
    name = request.match_info.get('phrase', '')
    try:
        name = base64.b64decode(name)
        name = name.decode('utf-8')
    except binascii.Error:
        return web.HTTPBadRequest(
            text='Search phrase "{}" should be in base64 format.'.format(name)
        )

    db = request.app['db']
    posts_analytic = await get_posts_analytic_by_phrase(db, name)
    results = gen_analytic_result(posts_analytic)

    return web.json_response(
        data={"search_results": results},
        content_type='application/json'
    )
