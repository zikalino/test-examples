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
  browser = await launch({"executablePath": EXECUTABLE_LOCATION})

  async with websockets.connect(browser.wsEndpoint) as websocket:

    response = await send_and_wait_for_response(
        websocket,
        None,
        'SystemInfo.getInfo',
        {}
    )

    response = await send_and_wait_for_response(
        websocket,
        None,
        'SystemInfo.getProcessInfo',
        {}
    )


asyncio.get_event_loop().run_until_complete(main())
