import urllib.request
import urllib.error
import requests
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def post_request(url, headers, params=None, data=None):
#  if query is not None:
#    query = urllib.parse.urlencode(query)
#    url = "{}?{}".format(url, query)
#  if params is not None:
#    data = json.dumps(params).encode("utf-8")
#  else:
#    data = None

  if data is not None:
    data = json.dumps(data).encode("utf-8")
      
#  request = urllib.request.Request(
#    url,
#    method = "POST",
#    data=data, 
#    headers=headers
#  )
  
  try:
    response = requests.post(
      url,
      headers=headers,
      params=params,
      data=data
    )
  except requests.RequestException as e:
    logging.info(get_members(e))
    logging.info(e)
  else:
    logging.info(response.status_code)
    logging.info(response.json())
    
    status = response.status_code
    resp_data = response.json()
    if status == 200:
      return resp_data
    elif status in [400, 401, 403, 404]:
      message = resp_data.get("message")
      error_messages = resp_data.get("error_messages")[0]
      
      if message is not None:
        raise Exception(message)
      elif error_messages is not None:
        raise Exception(error_messages)
      else:
        raise Exception("Something wrong!")
    else:
      raise Exception("Something wrong!")
    
#    with urllib.request.urlopen(request) as response:
#      data = json.loads(response.read().decode("utf-8"))
#      return data
    
#  except urllib.error.HTTPError as err:
#    logging.info("!!! err,, {}".format(err.reason))
#    logging.info("!!! data,, {}".format(data))
    
#    if err.code in [400, 401, 403, 404]:
#      if data.get("error_messages") is not None:
#        raise Exception(data.get("error_messages")[0])
#      elif data.get("message") is not None:
#        raise Exception(data.get("message"))
#      else:
#        raise Exception("Failed to send/get request, something wrong!")
#    else:
#      raise Exception("Failed to send/get request, something wrong!")
      
#  except urllib.error.URLError as err:
    
#    reason = err.reason
#    if reason is not None:
#      raise Exception(reason)
#    else:
#      raise Exception("Failed to send/get request, something wrong!")

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
