import requests
import os
import simplejson as json
token = os.getenv('TELEGRAM_TOKEN')

def send_telegram(data):
    print(token)
    #메세지 받기
    get_url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)
    send_url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
    response = json.loads(requests.get(get_url).text)
    print(response)
    chat_id = response["result"][-1]["message"]["from"]["id"]
    print(chat_id)

    #메세지 보내기
    requests.get(send_url, params={"chat_id" : chat_id, "text" : f"title:{data["title"]}\nlink:{data["link"]}\n신호:{data["result"]}"})