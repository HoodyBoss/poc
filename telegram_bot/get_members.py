from telethon import TelegramClient, sync
import asyncio
import pandas as pd
from datetime import datetime as dt, timedelta
import datetime

api_id = '25478541'
api_hash = '0c90201d36f55c231f2ebe5765897061'
BOT_TOKEN = '6284867484:AAFfIzE6O-9EZT-6d0bVHAx1vo9P5YJPvXk'
group_id = -1001877079626 #-1001781939396

# client = TelegramClient('DeepOceanTel', api_id, api_hash).start()

async def get_users(client, group_id):
    members = []
    # async for user in client.iter_participants(group_id):
    #     if not user.deleted:
    #         # print("id:", user.id, "username:", user.username) 
    #         print("'"+str(user.id)+"'") 
    #         members.append({"user_id": user.id, "user_name": user.username})

    # df = pd.DataFrame.from_records(members)
    # now = dt.now()
    # # csv_filename = now.strftime("%Y%m%d%H%M%S%f")
    # csv_filename = now.strftime("%Y%m%d")
    # df.to_csv(f"csv/{csv_filename}.csv", index=False)
    
    process_csv()

def process_csv():
    now = dt.now()
    # csv_filename = now.strftime("%Y%m%d%H%M%S%f")
    yesterday = now - timedelta(days=1)
    yesterday_csv = yesterday.strftime("%Y%m%d")
    yesterday_df = pd.read_csv(f"csv/{yesterday_csv}.csv")
    
    today_csv = now.strftime("%Y%m%d")
    today_df = pd.read_csv(f"csv/{today_csv}.csv")

    in_member = today_df.merge(yesterday_df, how='left', indicator='ind').query('ind=="left_only"')
    in_member.to_csv(f"csv/in_member_{today_csv}.csv", index=False)
    print("In member::", in_member)
    out_member = yesterday_df.merge(today_df, how='left', indicator='ind').query('ind=="left_only"')
    out_member.to_csv(f"csv/out_member_{today_csv}.csv", index=False)
    print("Out member::", out_member)

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=BOT_TOKEN)

with bot:
    asyncio.get_event_loop().run_until_complete(get_users(bot, group_id))
