import websocket, json, time, requests
import hashlib, jwt, uuid
import math
from urllib.parse import urlencode, unquote
import os
from datetime import datetime
import sys

sys.path.insert(0, '../tradeAlgorithm')
from get_account import account_data
from get_order_list import ordered_data
from dataPrepare import prepareData
from predictModel import fngModel, trendPredictModel
try:
    import thread
except ImportError:
    import _thread as thread


access_key = ''
secret_key = ''

def on_message(ws, message):
    print(message)
    if datetime.now().minute == 0:
        df = prepareData()
        if df['signal'].iloc[-1] == True and df['signal'].iloc[-2] == False:
            print('매수?')
            # voting algorithm 가져와..
            fngIndex = fngModel()
            trendIndex = trendPredictModel()
            if trendIndex >= 0: # 공포탐욕지수는 활용법 (threshold) 조금 더 생각해보자
                print('매수!!!')
                CURRENT_PRICE = 0
                MY_BULLET = account_data.balance # 현재 장전된 총알 (지갑 총량)

                params = {
                    'market': 'KRW-BTC',
                    'side': 'bid',
                    'ord_type': 'price',
                    'price': MY_BULLET,
                }
                query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

                m = hashlib.sha512()
                m.update(query_string)
                query_hash = m.hexdigest()

                payload = {
                    'access_key': access_key,
                    'nonce': str(uuid.uuid4()),
                    'query_hash': query_hash,
                    'query_hash_alg': 'SHA512',
                }

                jwt_token = jwt.encode(payload, secret_key)
                authorization = 'Bearer {}'.format(jwt_token)
                headers = {
                    'Authorization': authorization,
                }

                res = requests.post('https://api.upbit.com/v1/orders', json=params, headers=headers)
                res.json()


            

        elif df['signal'].iloc[-1] == False and df['signal'].iloc[-2] == True:
            print('매도?')
            #votine algorithm 가져와...
            fngIndex = fngModel()
            trendIndex = trendPredictModel()
            if trendIndex < 0:
                print('매도!')
                params = {
                    'market': 'KRW-BTC',
                    'side': 'ask',
                    'ord_type': 'market',
                    'volume': ordered_data.volume
                }
                query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

                m = hashlib.sha512()
                m.update(query_string)
                query_hash = m.hexdigest()

                payload = {
                    'access_key': access_key,
                    'nonce': str(uuid.uuid4()),
                    'query_hash': query_hash,
                    'query_hash_alg': 'SHA512',
                }

                jwt_token = jwt.encode(payload, secret_key)
                authorization = 'Bearer {}'.format(jwt_token)
                headers = {
                    'Authorization': authorization,
                }

                res = requests.post('https://api.upbit.com/v1/orders', json=params, headers=headers)
                res.json()




def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        ws.send(json.dumps(
            [{"ticket": "test"}, {"type": "ticker", "codes": ["KRW-BTC"]}]))
    thread.start_new_thread(run, ())


websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://api.upbit.com/websocket/v1/orders",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open
print(ws.on_open)
ws.run_forever()