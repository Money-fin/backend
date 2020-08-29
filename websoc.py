import os
from json import dumps
import asyncio
import websockets
from telegram import send_telegram
from receive_data import receive_result
import time
import requests
import urllib
import os
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from helper import KafkaHelper

def new_crawl(link):
  url = link

  item_info = requests.get(url).text
  soup = BeautifulSoup(item_info, 'html.parser')
  title = soup.select('div.content03 header.title-article01 h1')[0].get_text()
  time = soup.select('div.content03 header.title-article01 p')[0].get_text()[4:]
  img_url = f"https:{soup.select('div.img-con span img')[0]['src']}"
  raw_content = soup.select('div.story-news.article')
  # print(raw_content)
  content_p = [item.select("p") for item in raw_content]
  content_text = [item.get_text().strip() for item in content_p[0]]
  content = "\n".join(content_text[1:])
  content = content.replace("'","")
  data_dict = {
    "title": title,
    "content": content,
    "link": link
  }
  data_dict["time"] = time
  data_dict["img_url"] = img_url
  return data_dict

class Server:

    def get_port(self):
        return os.getenv('WS_PORT', '9998')

    def get_host(self):
        return os.getenv('WS_HOST', '0.0.0.0')


    def start(self):
        return websockets.serve(self.handler, self.get_host(), self.get_port())

    async def handler(self, websocket, path):
        print("connected!")
        data = receive_result()
        print(data)
        chat_data = new_crawl(data["link"])
        chat_data["result"] = data["result"]
        send_telegram(data)
        await websocket.send(f"{chat_data}")

if __name__ == '__main__':
  ws = Server()
  asyncio.get_event_loop().run_until_complete(ws.start())
  asyncio.get_event_loop().run_forever()