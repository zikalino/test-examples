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

async def launch_and_connect(user_dir=None,
                             additional_args={}):

  global websocket

  args = {'executablePath': EXECUTABLE_LOCATION,
          'ignoreDefaultArgs': True
          } | additional_args
  

  if user_dir:
    args['args'].append('--user-data-dir=' + user_dir)

  browser = await launch(args)


  return await websockets.connect(browser.wsEndpoint)
  
async def send(ws, msg):
    await ws.send(json.dumps(msg))

async def receive_response(ws, msg):
    response = {}
    while (not 'id' in response) or (response['id'] != msg['id']):

      if 'method' in response:
        if response['method'] == 'Runtime.consoleAPICalled':
          process_log_message(response)
        # XXX - store if response was unrelated
        #if json.dumps(response) != '{}':
        #  print('### ' + json.dumps(response))
      response = json.loads(await ws.recv())
    return response

def process_log_message(msg):
  if msg['params']['type'] == 'log':
    args = msg['params']['args']
    for a in args:
      print("## " + a['value'])

async def get_message(ws):
  while True:
    msg = json.loads(await ws.recv())
    if 'method' in msg:
      if msg['method'] == 'Runtime.consoleAPICalled':
        process_log_message(msg)

def get_next_id():
  global next_id
  next_id += 1
  return next_id
