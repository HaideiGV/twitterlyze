from aiohttp import web

async def health_handler(request):
    return web.Response(text="It's alive.")
