# send-message-to-telegram.py
# by www.ShellHacks.com

import requests

telegramApi = '6017754651:AAHQH9seNbhq-m-GVyH81OSVnaHYJ7wUJNU'
url = f"https://api.telegram.org/bot{telegramApi}/getUpdates"
result = requests.get(url).json()

for x in result.keys():
    if x == "result" and result["result"]:
        chat_id = result["result"]["sender_chat"]["id"] if "result" in result and "sender_chat" in result["result"] and "id" in result["result"]["sender_chat"] else "0"
print(chat_id)
chat_id = 1763498590

def send_to_telegram(message):

    apiURL = f'https://api.telegram.org/bot{telegramApi}/sendMessage'

    try:
        # response = requests.post(apiURL, json={'chat_id': chat_id, 'text': message})
        telegram_endpoint='https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s'
        url = telegram_endpoint % (telegramApi, chat_id, message)
        response=requests.get(url, timeout=10)
        print(response.text)
    except Exception as e:
        print(e)

send_to_telegram("Hello from Python! naja")