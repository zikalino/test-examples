## demo.py

import asyncio
import websockets
import json
import time
from connection import launch_and_connect, get_next_id, send, receive_response
from generic import attach_to_target

async def main():
  ws = await launch_and_connect()

  time.sleep(20)
  msg = {
    'id': get_next_id(),
    'method': 'Target.getTargets',
    'params': {
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
        }
  }

  await send(ws, msg)
  response = await receive_response(ws, msg)
  print(json.dumps(response, indent=2))

  for l in response['result']['targetInfos']:
    session_id = await attach_to_target(ws, l['targetId'])

    msg = {
      'id': get_next_id(),
      'sessionId': session_id,
      'method': 'Page.getAppManifest'
    }
    await send(ws, msg)
    response = await receive_response(ws, msg)
    print(json.dumps(response, indent=2))



asyncio.get_event_loop().run_until_complete(main())
