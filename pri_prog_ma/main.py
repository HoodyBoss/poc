import os
import sys
import uuid
from google.cloud import firestore
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import pandas as pd
import requests
import json
import pytz

from datetime import datetime as dt

from deepocean_trade_api.common import *
from deepocean_trade_api.common.config import *

_conf = ConfigManager()
_conf = _conf.load_config()
logger = DOLogger(_env=_conf["logs"]["env"], log_name="TRANSACTION_REPORT", level=_conf["logs"]["level"])


from flask import Flask
from flask import request

app = Flask(__name__)

PRJ_NOTFICATION_GATEWAY_URL= os.getenv("PRJ_NOTFICATION_GATEWAY_URL")
PRJ_NOTFICATION_GATEWAY_KEY= os.getenv("PRJ_NOTFICATION_GATEWAY_KEY")

PRJ_SECRET_GATEWAY_URL= os.getenv("PRJ_SECRET_GATEWAY_URL")
PRJ_SECRET_GATEWAY_KEY= os.getenv("PRJ_SECRET_GATEWAY_KEY")

bkk_timezone = pytz.timezone("Asia/Bangkok") 
time_format = "%Y%m%d%H%M%S-%f"
input_dateformat = "%Y-%m-%dT%H:%M:%S.%f+0000"
output_dateformat = "%Y-%m-%d %H:%M:%S"
ADMIN_EMAIL="super.admin@deepocean.fund"
MANTA_ADMIN_EMAIL="manta.admin@deepocean.fund"
MOLLY_ADMIN_EMAIL="molly.admin@deepocean.fund"
MANTA_STRATEGY_ID="MANTA001"
MOLLY_STRATEGY_ID="MOLLY001"

allow_users = ["56faacc5-bff2-4f06-a932-526d04ff80eb","aeb4103e-01ab-4890-b20e-201fdb6606a5"
, "2bc93585-600d-4cb1-9504-492e09f17b72","3c21218b-cf7c-4a3d-95f9-489af9098569"
,"462d7300-2271-4ffc-b846-a8e0fad225f7",""]

@app.route("/", methods=['GET'])
def index():
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Origin': '*'
    }

    return ("Run private program maintenance completely", 200, headers) 

@app.route("/update/trades", methods=['GET'])
def update_trades():
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    
    # # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Origin': '*'
    }

    # logger.debug(f'Input data from another service>>>{json_data}')
    try:
        
        db = firestore.Client()
        
        #get subscriptions data first
        trades_ref = db.collection(u'trades')
        trades = trades_ref.stream()

        for doc_ref in trades:
            doc = trades_ref.document(doc_ref.id)
            data = doc_ref.to_dict()
            print("doc id.::", doc_ref.id, " - subscription :",data["subscription_id"] )
            if "transaction_timestamp" not in data:
                doc.update({"transaction_timestamp": data["transaction_date"]})
            
        # if len(res_data) > 0:
        return ({"res_data": "update trade timestamp success"}, 200, headers) 

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f'"error": {e}, "line no.":"{exc_tb.tb_lineno}"')
        return ({"res_data": "Internal server error"}, 500, headers) 

if __name__ == "__main__":
    app.run( host="0.0.0.0", port=int(os.environ.get("PORT", 8098)))