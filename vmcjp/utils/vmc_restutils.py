import urllib.request
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
  
  with urllib.request.urlopen(request) as response:
    if response.getcode() == 200:
      data = json.loads(response.read().decode("utf-8"))
      return data

def get_request(url, headers):
  request = urllib.request.Request(
    url,
    method = "GET",
    headers=headers
  )
  with urllib.request.urlopen(request) as response:
    if response.getcode() == 200:
      data = json.loads(response.read().decode("utf-8"))
      return data
