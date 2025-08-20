from connection import send, receive_response, get_next_id

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

  return await attach_to_target(ws, target_id)

async def get_target_info(ws, target_id):
  msg = {
    'id': get_next_id(),
    'method': 'Target.getTargetInfo',
    'params': {
      'targetId': target_id
    }
  }
  await send(ws, msg)
  response = await receive_response(ws, msg)
  return response

async def attach_to_target(ws, target_id):
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

async def close_target(ws, target_id):
  msg = {
    'id': get_next_id(),
    'method': 'Target.closeTarget',
    'params': {
      'targetId': target_id
    }
  }
  await send(ws, msg)
  response = await receive_response(ws, msg)
  if 'result' in response['result'] and 'value' in response['result']['result']:
    return response['result']['result']['value']
  else:
    return response['result']

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
  if 'value' in response['result']['result']:
    return response['result']['result']['value']
  else:
    return response['result']['result']

async def enable_log(ws, session_id):
  msg = {
    'id': get_next_id(),
    'method': 'Log.enable',
    'sessionId': session_id,
    'params': {}
  }

  await send(ws, msg)
  response = await receive_response(ws, msg)

