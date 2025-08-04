import asyncio
import json
import time
from connection import launch_and_connect, send, receive_response, get_next_id

async def main():

  ws = await launch_and_connect()

  msg = {
    'id': get_next_id(),
    'method': 'SystemInfo.getInfo'
  }
  await send (ws, msg)
  response = await receive_response(ws, msg)
  print(json.dumps(response, indent=2))

  for i in range(20):
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
    time.sleep(5)


asyncio.get_event_loop().run_until_complete(main())
