## demo.py

import asyncio
import websockets
import json
import time
from pyppeteer import launch
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from settings import EXECUTABLE_LOCATION

next_id = 1

async def send_and_wait_for_response(websocket, session_id, method, params):
    global next_id
    # send message
    message = { 'id': next_id,
                'method': method,
                'params': params
              }
    if session_id:
        message['sessionId'] = session_id

    await websocket.send(json.dumps(message))

    # and await response, just dump all messages without appropriate id
    response = {}
    while (not 'id' in response) or (response['id'] != next_id):
        response = json.loads(await websocket.recv())
        print(f" ... received: ")
        print(response)

    next_id += 1
    return response

async def main():
  global next_id
  
  # path to extension to be loaded
  extension_path = str(Path(__file__).resolve().parent.joinpath('extension'))
  print(extension_path)

  browser = await launch({'executablePath': EXECUTABLE_LOCATION,
                          'ignoreDefaultArgs': True,
                          'args': ['--load-extension=' + extension_path]})

  async with websockets.connect(browser.wsEndpoint) as websocket:
    print("CONNECTED....")

    #response = await send_and_wait_for_response(
    #    websocket,
    #    None,
    #    'Extensions.loadUnpacked',
    #    {
    #        'path': extension_path
    #    }
    #)

    for i in range(10):
        response = await send_and_wait_for_response(
                websocket,
                None,
                'Target.getTargets',
                {
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
                })

        #print("slepping 60")
        #time.sleep(60)
        #print("continue")

        print('----------------------------- ' + str(len(response['result']['targetInfos'])))
        for l in response['result']['targetInfos']:
            if 'koi' in l['url']:
                print(l['targetId'] + " | " + l['type']  + ' | ' + l['title'] + ' | ' + l['url'])
        time.sleep(5)
    

asyncio.get_event_loop().run_until_complete(main())
