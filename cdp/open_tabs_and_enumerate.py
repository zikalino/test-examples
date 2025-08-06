import asyncio
import json
from connection import launch_and_connect, send, receive_response, get_next_id

async def create_and_attach_tab(ws, url):
  msg = {
    'id': get_next_id(),
    'method': 'Target.createTarget',
    'params': {
      'url': url
    }
  }
  await send(ws, msg)
  response = await receive_response(ws, msg)

  target_id = response['result']['targetId']

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

async def evaluate(ws, session_id, expression):
  msg = {
    'id': get_next_id(),
    'method': 'Runtime.evaluate',
    'sessionId': session_id,
    'params': {
      'expression': expression
    }
  }

  await send(ws, msg)
  response = await receive_response(ws, msg)
  return response['result']['result']['value']

async def main():

  ws = await launch_and_connect()

  session_id = await create_and_attach_tab(ws, 'https://google.com')

  result = await evaluate(ws, session_id, "'Result is ' + 'OK'")

  print(json.dumps(result, indent=2))



asyncio.get_event_loop().run_until_complete(main())
