## demo.py

import asyncio
import websockets
import json
import time
import sys

from pyppeteer import launch
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from settings import EXECUTABLE_LOCATION

next_id = 1
websocket = None

async def launch_and_connect(user_dir=None):

  global websocket
  # path to extension to be loaded
  extension_path = str(Path(__file__).resolve().parent.joinpath('extension'))

  args = {'executablePath': EXECUTABLE_LOCATION,
          'ignoreDefaultArgs': True,
          'args': ['--load-extension=' + extension_path,
          '--enable-automation',
          '--enable-unsafe-extension-debugging'
          ]}

  if user_dir:
    args['args'].append('--user-data-dir=' + user_dir)

  browser = await launch(args)


  return await websockets.connect(browser.wsEndpoint)
  
async def send(ws, msg):
    await ws.send(json.dumps(msg))

async def receive_response(ws, msg):
    response = {}
    while (not 'id' in response) or (response['id'] != msg['id']):
        # XXX - store if response was unrelated
        response = json.loads(await ws.recv())
    return response

def get_next_id():
  global next_id
  next_id += 1
  return next_id
