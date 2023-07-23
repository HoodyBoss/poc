from jugaad_data.nse import NSELive
from tgsend import Telegram, ParseMode
import time
import os

def get_prices(stockSymbol):
    '''A function to get live prices using jugaad_data library'''
    n = NSELive()
    q = n.stock_quote(stockSymbol)
    return q['priceInfo']['lastPrice']

def send_telegram_message(message):
    # token and chat ID will be searched in config files if not specified here
    telegram = Telegram(os.getenv("TGSEND_TOKEN"), os.getenv("TGSEND_CHATID"))
    # send a text message
    telegram.send_message(
        str(message),
        title="Price of HDFC",
        parse_mode=ParseMode.MARKDOWN
    )
    # ts.send(messages = [str(message)])
    # pass

live_prices = []
count = 0

while True: 
    current_price = get_prices('HDFC')
    live_prices.append(current_price)
    count = count + 5
    print(f'{count} Minutes Done')

    if len(live_prices) == 5:
        avg_price = round((sum(live_prices[-5:])/len(live_prices[-5:])),2)
        if count == 5:
            send_telegram_message(f'The Average Price of HDFC For Last 1 Minutes is {avg_price}')
            #print(f'The Average Price of HDFC For Last 5 Minutes is {avg_price}')
            count = 0
            live_prices.clear()

    time.sleep(60)
