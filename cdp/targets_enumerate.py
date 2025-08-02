## demo.py

import asyncio
import websockets
import json
import time
from pyppeteer import launch

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
    print("CONNECTED....")

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
                    {
                        "exclude": True,
                        "type": "page"
                    },
                    {
                        "exclude": False
                    }
                ]
            })

    #print("slepping 60")
    #time.sleep(60)
    #print("continue")

    for l in response['result']['targetInfos']:
        # if l['url'] == '':
          #print("SLEPPING BEFORE ATTACHING")
          #time.sleep(60)
          #print("SLEPPING IS OVER")

          print('============================================================== ATTACHING TO:')
          print(l)
          response = await send_and_wait_for_response(
                websocket,
                None,
                'Target.attachToTarget',
                {
                    'targetId': l['targetId'],
                    'flatten': True
                }
            )

          sessionId = response['result']['sessionId']

          # autoattach
          print('------------------------------- AUTO ATTACH:')
          response = await send_and_wait_for_response(
                websocket,
                sessionId,
                'Target.setAutoAttach',
                {
                    "autoAttach": True,
                    "flatten": True,
                    "waitForDebuggerOnStart": False
                }
          )

          # now we are attached, try to enable page
          print('------------------------------- ENABLING PAGE:')
          response = await send_and_wait_for_response(
                websocket,
                sessionId,
                'Page.enable',
                {}
          )

          # now we are attached, try to enable log
          print('------------------------------- ENABLING LOG:')
          response = await send_and_wait_for_response(
                websocket,
                sessionId,
                'Log.enable',
                {}
          )


          # now we are attached, try to enable log
          print('------------------------------- ENABLING RUNTIME:')
          response = await send_and_wait_for_response(
                websocket,
                sessionId,
                'Runtime.enable',
                {}
          )


asyncio.get_event_loop().run_until_complete(main())
