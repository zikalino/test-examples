import asyncio
import json
from connection import launch_and_connect
from generic import create_and_attach_tab, evaluate

async def main():

  ws = await launch_and_connect()

  session_id = await create_and_attach_tab(ws, 'https://google.com')

  result = await evaluate(ws, session_id, "'Result is ' + 'OK'")

  print(json.dumps(result, indent=2))


asyncio.get_event_loop().run_until_complete(main())
