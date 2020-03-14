import requests
import urllib.request
import json
import logging

def post_request(url, headers, query=None, params=None):
  if query is not None:
    query = urllib.parse.urlencode(query)
    url = "{}?{}".format(url, query)
  if params is not None:
    data = json.dumps(params).encode("utf-8")
    
  request = urllib.request.Request(
    url,
    data=data, 
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
