import urllib.request
import urllib.error
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def post_request(url, headers, query=None, params=None):
  if query is not None:
    query = urllib.parse.urlencode(query)
    url = "{}?{}".format(url, query)
  if params is not None:
    data = json.dumps(params).encode("utf-8")
  else:
    data = None

  request = urllib.request.Request(
    url,
    method = "POST",
    data=data, 
    headers=headers
  )
  
  try:
    
    with urllib.request.urlopen(request) as response:
      data = json.loads(response.read().decode("utf-8"))
      return data
    
  except urllib.error.HTTPError as err:
    logging.info(data)
    
    if err.code in [400, 401, 403, 404]:
      if data.get("error_messages") is not None:
        raise Exception(data.get("error_messages")[0])
      elif data.get("message") is not None:
        raise Exception(data.get("message"))
      else:
        raise Exception("Failed to send/get request, something wrong!")
    else:
      raise Exception("Failed to send/get request, something wrong!")
      
  except urllib.error.URLError as err:
    
    reason = err.reason
    if reason is not None:
      raise Exception(reason)
    else:
      raise Exception("Failed to send/get request, something wrong!")

def get_request(url, headers, params=None):
  if params is not None:
    query = urllib.parse.urlencode(params)
    url = "{}?{}".format(url, query)
    
  request = urllib.request.Request(
    url,
    method = "GET",
    headers=headers
  )
  
  try:
    
    with urllib.request.urlopen(request) as response:
      data = json.loads(response.read().decode("utf-8"))
      return data
    
  except urllib.error.HTTPError as err:
    
    if err.code in [400, 401, 403, 404]:
      if data.get("error_messages") is not None:
        raise Exception(data.get("error_messages")[0])
      elif data.get("message") is not None:
        raise Exception(data.get("message"))
      else:
        raise Exception("Failed to send/get request, something wrong!")
    else:
      raise Exception("Failed to send/get request, something wrong!")
      
  except urllib.error.URLError as err:
    
    reason = err.reason
    if reason is not None:
      raise Exception(reason)
    else:
      raise Exception("Failed to send/get request, something wrong!")
