from aiohttp import web, WSMsgType
import json


class WebSocket(web.View):
	async def get(self):
		ws = web.WebSocketResponse()
		await ws.prepare(self.request)
		self.id = ''
		async for msg in ws:
			if msg.type == WSMsgType.TEXT:
				if msg.data == 'ping':
					await ws.pong(b'pong')
				else:
					mes = json.loads(msg.data)
					if mes['mtype'] == 'INIT':
						if 'websockets' not in self.request.app:
							self.request.app['websockets'] = {}
						for _ws in self.request.app['websockets'].values():
							await _ws.send_json(
									{'mtype': 'USER_ENTER', 'id': mes['id']})
						self.request.app['websockets'][mes['id']] = ws
						self.id = mes['id']
					elif mes['mtype'] == 'TEXT':
						if not mes['to']:
							for _ws in self.request.app['websockets']:
								if _ws != mes['id']:
									await self.request.app['websockets'][
										_ws].send_json(
											{'mtype': 'MSG', 'id': mes['id'],
											 'text': mes['text']})
						elif mes['to'] and mes['to'] in self.request.app['websockets']:
							await self.request.app['websockets'][
								mes['to']].send_json(
									{'mtype': 'DM', 'id': mes['id'],
									 'text': mes['text']})

		self.request.app['websockets'].pop(self.id)
		for _ws in self.request.app['websockets'].values():
			await _ws.send_json(
					{'mtype': 'USER_LEAVE', 'id': self.id})
		await ws.close()
		return ws


class WSChat:
	def __init__(self, host='0.0.0.0', port=8080):
		self.host = host
		self.port = port
		self.conns = {}

	@staticmethod
	async def main_page(request):
		return web.FileResponse('./index.html')

	def run(self):
		app = web.Application()

		app.router.add_get('/', self.main_page)
		app.router.add_get('/chat', WebSocket)

		web.run_app(app, host=self.host, port=self.port)


if __name__ == '__main__':
	WSChat().run()
