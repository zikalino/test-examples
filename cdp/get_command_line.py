import asyncio
import json
import time
import os
from connection import launch_and_connect, send, receive_response, get_next_id
from pathlib import Path

async def main():

  dir = os.path.join(Path.cwd(), "tmp")
  ws = await launch_and_connect(user_dir=dir)

  msg = {
    'id': get_next_id(),
    'method': 'Browser.getBrowserCommandLine'
  }
  await send(ws, msg)
  response = await receive_response(ws, msg)
  print(json.dumps(response['result'], indent=2))

asyncio.get_event_loop().run_until_complete(main())
