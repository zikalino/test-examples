import asyncio
from connection import launch_and_connect, send, receive_response, get_next_id

async def main():

  ws = await launch_and_connect()

  msg = {
    'id': get_next_id(),
    'method': 'Target.createTarget',
    'params': {
      'url': 'https://onet.pl'
    }
  }
  await send(ws, msg)
  response = await receive_response(ws, msg)

  msg = {
    'id': get_next_id(),
    'method': 'Target.createTarget',
    'params': {
      'url': 'https://gazeta.pl'
    }
  }
  await send(ws, msg)
  response = await receive_response(ws, msg)

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

  for l in response['result']['targetInfos']:
    print(l['targetId'] + " | " + l['type']  + ' | ' + l['title'] + ' | ' + l['url'])

asyncio.get_event_loop().run_until_complete(main())
