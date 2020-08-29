import os
import asyncio
import websockets
from telegram import send_telegram
from receive_data import receive_result
import time
class Server:

    def get_port(self):
        return os.getenv('WS_PORT', '9385')

    def get_host(self):
        return os.getenv('WS_HOST', '0.0.0.0')


    def start(self):
        return websockets.serve(self.handler, self.get_host(), self.get_port())

    async def handler(self, websocket, path):
        print('server received :', "123")
        while True:
            time.sleep(10)
            data = receive_result()
            send_telegram(data)
            await websocket.send(data)

if __name__ == '__main__':
  ws = Server()
  asyncio.get_event_loop().run_until_complete(ws.start())
  asyncio.get_event_loop().run_forever()