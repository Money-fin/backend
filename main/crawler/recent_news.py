import requests
import urllib
import os
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from main.kafka.helper import KafkaHelper

def new_crawl(link, kafka=False):
  url = link

  item_info = requests.get(url).text
  soup = BeautifulSoup(item_info, 'html.parser')
  title = soup.select('div.content03 header.title-article01 h1')[0].get_text()
  time = soup.select('div.content03 header.title-article01 p')[0].get_text()
  img_url = f"https:{soup.select('div.img-con span img')[0]['src']}"
  raw_content = soup.select('div.story-news.article')
  # print(raw_content)
  content_p = [item.select("p") for item in raw_content]
  content_text = [item.get_text().strip() for item in content_p[0]]
  content = "\n".join(th_data2[1:])
  data_dict = {
    "title": title,
    "content": content,
    "link": link
  }
  if kafka:
    KafkaHelper.pub_ninput(data_dict)
  else:
    data_dict["time"] = time
    data_dict["img_url"] = img_url
    return data_dict

def recent_new_check():
  past_list = ""
  while True:
    url = f'https://www.yna.co.kr/news?site=navi_latest_depth01'
    item_info = requests.get(url).text
    soup = BeautifulSoup(item_info, 'html.parser')
    new_a_tag = soup.select('div.list-type038 ul')[0].select("li")[0].select("div div a.tit-wrap") 
    current_link = f"https:{new_a_tag[0]['href']}"
    if past_list == current_link:
      continue
    else:
      new_crawl(current_link, True)
      past_list = current_link

recent_new_check()