import urllib.request
import urllib.error
import json

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
    return None
  except urllib.error.URLError as err:
    return None

def get_request(url, headers):
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
    return None
  except urllib.error.URLError as err:
    return None
