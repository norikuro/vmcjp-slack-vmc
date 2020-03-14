import requests
import urllib.request
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def post_request(url, headers, query=None, params=None):
  logging.info("!!! query: {}".format(query))
  if query is not None:
    _query = urllib.parse.urlencode(query)
    _url = "{}?{}".format(url, _query)
    logging.info("!!! url: {}".format(_url))
  if params is not None:
    data = json.dumps(params).encode("utf-8")
  else:
    data = None

  request = urllib.request.Request(
    _url,
    method = "POST",
#    data=data, 
    headers=headers
  )
  
#  response = urllib.request.urlopen(request)
  with urllib.request.urlopen(request) as response:
    data = response.read().decode("utf-8")
#  response = requests.post(
#    url,
#    headers=headers,
#    params=params
#  )
#  logging.info(response.text)
#  if response is not None:
#    data = response.json()
#    if response.status_code == 200:
#      return data
  return data

def get_request(url, headers):
  response = requests.get(
    url,
    headers=headers
  )
  if response is not None:
    data = response.json()
    if response.status_code == 200:
      return data
