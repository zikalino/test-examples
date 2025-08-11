import asyncio
import json
import time
import os
from connection import launch_and_connect, send, receive_response, get_next_id
from generic import close_target
from pathlib import Path

async def main():

  dir = os.path.join(Path.cwd(), "tmp")
  ws = await launch_and_connect(user_dir=dir)

  msg = {
    'id': get_next_id(),
    'method': 'SystemInfo.getProcessInfo'
  }
  await send (ws, msg)
  response = await receive_response(ws, msg)
  print('------------------------------------------------')
  print('NUMBER OF PROCESSES: ' + str(len(response['result']['processInfo'])))
  print('------------------------------------------------')
  for process in response['result']['processInfo']:
    print(json.dumps(process))

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
  targets = response['result']['targetInfos']
  print('------------------------------------------------')
  print('TARGETS:')
  print('------------------------------------------------')
  printed = set(())
  for l in targets:
    print(l['type'] + ' ' + l['url'])

asyncio.get_event_loop().run_until_complete(main())
