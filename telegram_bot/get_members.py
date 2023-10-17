from telethon import TelegramClient, sync
import asyncio
import pandas as pd
from datetime import datetime as dt, timedelta
import datetime
import sys

api_id = '25478541'
api_hash = '0c90201d36f55c231f2ebe5765897061'
BOT_TOKEN = '6284867484:AAFfIzE6O-9EZT-6d0bVHAx1vo9P5YJPvXk'

#declare group id here, add new group by add new array item
groups = [-1001877079626, -1001781939396, -1001967606094, -1001851806627]

#main method to access tg group then list member who is not deleted from group
async def get_users(client, group_id):
    members = []
    try:
        async for user in client.iter_participants(group_id):
            if not user.deleted:
                # print("id:", user.id, "username:", user.username) 
                print("'"+str(user.id)+"'") 
                members.append({"user_id": user.id, "user_name": user.username})

        df = pd.DataFrame.from_records(members)
        now = dt.now()
        # csv_filename = now.strftime("%Y%m%d%H%M%S%f")
        csv_filename = now.strftime("%Y%m%d")
        df.to_csv(f"csv/{csv_filename}{group_id}.csv", index=False)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Get user : ", e, ", line no.::", exc_tb.tb_lineno)
    
    process_csv(group_id)

#csv process to calculate new member or left the group member compare between today and yesterday
def process_csv(group_id):
    try:
        now = dt.now()
        # read yesterday member list of the group
        yesterday = now - timedelta(days=1)
        yesterday_csv = yesterday.strftime("%Y%m%d")
        try:
            with open(f"csv/{yesterday_csv}{group_id}.csv", "x") as f:
                f.write("user_id,user_name")
                f.close()
        except:
            pass
        yesterday_df = pd.read_csv(f"csv/{yesterday_csv}{group_id}.csv")
        
        # read today member list of the group
        today_csv = now.strftime("%Y%m%d")
        try:
            with open(f"csv/{today_csv}{group_id}.csv", "x") as f:
                f.write("user_id,user_name")
                f.close()
        except:
            pass
        today_df = pd.read_csv(f"csv/{today_csv}{group_id}.csv")

        # compare by today member and yesterday member who is in today list, determine is member left the group
        in_member = today_df.merge(yesterday_df, how='left', indicator='ind').query('ind=="left_only"')
        in_member.to_csv(f"csv/in_member_{today_csv}{group_id}.csv", index=False)
        print("In member::", in_member)
        
        # on the other hand, if member is in yesterday list only, determine who is new member
        out_member = yesterday_df.merge(today_df, how='left', indicator='ind').query('ind=="left_only"')
        out_member.to_csv(f"csv/out_member_{today_csv}{group_id}.csv", index=False)
        print("Out member::", out_member)
        
        try:
            with open(f"csv/inout_member_hist{group_id}.csv", "x") as f:
                f.write("date,in,out")
                f.close()
        except:
            pass
        
        df = pd.read_csv(f"csv/inout_member_hist{group_id}.csv")
        # print("in member len::", len(in_member.index), ":", "out_member len:", len(out_member.index))
        if len(in_member.index) > 0 or len(out_member.index) > 0:
            df.loc[len(df.index)] = [today_csv, in_member.to_json(), out_member.to_json()]
            df.to_csv(f"csv/inout_member_hist{group_id}.csv", index=False)
            
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Get user : ", e, ", line no.::", exc_tb.tb_lineno)

for group in groups:
    
    try:
        bot = TelegramClient('bot', api_id, api_hash).start(bot_token=BOT_TOKEN)
        with bot:
            asyncio.get_event_loop().run_until_complete(get_users(bot, group))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Main : ", e, ", line no.::", exc_tb.tb_lineno)
