## demo.py

import asyncio
import websockets
import json
import time
from pyppeteer import launch

from connection import launch_and_connect, send, receive_response, get_next_id

async def send_and_wait_for_response(websocket, session_id, method, params):
    global next_id
    # send message
    message = { 'id': next_id,
                'method': method,
                'params': params
              }
    if session_id:
        message['sessionId'] = session_id

    await websocket.send(message)

    # and await response, just dump all messages without appropriate id
    response = {}
    while (not 'id' in response) or (response['id'] != next_id):
        response = json.loads(await websocket.recv())
        print(f" ... received: ")
        print(response)

    next_id += 1
    return response

async def main():

  ws = await launch_and_connect()

  #response = await send_and_wait_for_response(
  #    websocket,
  #    None,
  #    'Extensions.loadUnpacked',
  #    {
  #        'path': extension_path
  #    }
  #)

  for i in range(100):
    msg = { 'id': get_next_id(),
            'method': 'Target.getTargets',
            'params': {
                    'filter': [
                        {
                        "exclude": False,
                        "type": "browser"
                        },
                        #{
                        #    "exclude": True,
                        #    "type": "page"
                        #},
                        {
                            "exclude": False
                        }
                    ]
                }
            }
    await send(ws, msg)
    response = await receive_response(ws, msg)

    print('----------------------------- ' + str(len(response['result']['targetInfos'])))
    for l in response['result']['targetInfos']:
        if 'knoh' in l['url']:
            print(l['targetId'] + " | " + l['type']  + ' | ' + l['title'] + ' | ' + l['url'])
    time.sleep(5)

asyncio.get_event_loop().run_until_complete(main())
