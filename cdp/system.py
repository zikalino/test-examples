import asyncio
from connection import launch_and_connect, send, receive_response, get_next_id

async def main():

  ws = await launch_and_connect()

  msg = {
    'id': get_next_id(),
    'method': 'SystemInfo.getInfo'
  }
  await send (ws, msg)
  response = await receive_response(ws, msg)

  msg = {
    'id': get_next_id(),
    'method': 'SystemInfo.getProcessInfo'
  }
  await send (ws, msg)
  response = await receive_response(ws, msg)

asyncio.get_event_loop().run_until_complete(main())
