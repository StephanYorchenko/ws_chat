#!/usr/bin/env python3

from aiohttp import web
# TODO


class WSChat:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.conns = {}

    async def main_page(self, request):
        return web.FileResponse('./index.html')

    # TODO

    def run(self):
        app = web.Application()

        app.router.add_get('/', self.main_page)

        # TODO

        web.run_app(app, host=self.host, port=self.port)


if __name__ == '__main__':
    WSChat().run()
