## demo.py

import asyncio
import websockets
import json
import time
from pyppeteer import launch

from connection import launch_and_connect, send, receive_response, get_next_id

async def attach_to_target(ws, target_id):
  msg = {
    'id': get_next_id(),
    'method': 'Target.attachToTarget',
    'params': {
      'targetId': target_id,
      'flatten': True
    }
  }
  await send(ws, msg)
  response = await receive_response(ws, msg)
  session_id = response['result']['sessionId']

  msg = {
    'id': get_next_id(),
    'method': 'Runtime.enable',
    'sessionId': session_id,
  }
  await send(ws, msg)
  response = await receive_response(ws, msg)
  return session_id


async def main():

  ws = await launch_and_connect()
  found = None

  while (not found):
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

    for l in response['result']['targetInfos']:
        if 'knoh' in l['url']:
            found = l['targetId']

    if not found:
        time.sleep(1)

  # found target --- attach
  await attach_to_target(ws, found)
  print ("Attached to popup!!")
  # attached to target
  time.sleep(20)


asyncio.get_event_loop().run_until_complete(main())
