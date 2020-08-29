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
import websocket
import thread
import time
import json

def new_crawl(link):
  url = link

  item_info = requests.get(url).text
  soup = BeautifulSoup(item_info, 'html.parser')
  title = soup.select('div.content03 header.title-article01 h1')[0].get_text()
  title = title.replace('"','')
  title = title.replace("'","")
  time = soup.select('div.content03 header.title-article01 p')[0].get_text()[4:]
  img_url = f"https:{soup.select('div.img-con span img')[0]['src']}"
  raw_content = soup.select('div.story-news.article')
  # print(raw_content)
  content_p = [item.select("p") for item in raw_content]
  content_text = [item.get_text().strip() for item in content_p[0]]
  content = "\n".join(content_text[1:])
  content = content.replace('"','')
  content = content.replace("'","")
  data_dict = {
    "title": title,
    "content": content,
    "link": link
  }
  data_dict["time"] = time
  data_dict["img_url"] = img_url
  return data_dict



def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        print("connected!")
        data = receive_result()
        print(data)
        chat_data = new_crawl(data["link"])
        chat_data["result"] = data["result"]
        send_telegram(data)
        ws.send(f"{chat_data}".replace("'",'"'))
        while True:
            time.sleep(1)
        ws.close()
        print("thread terminating...")

    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://random.example.com",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
