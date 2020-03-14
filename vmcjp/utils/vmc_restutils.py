import requests
import urllib.request
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def post_request(url, headers, params):
  request = urllib.request.Request(
    url,
    data=json.dumps(params).encode("utf-8"), 
    headers=headers
  )
  response = urllib.request.urlopen(request)
#  response = requests.post(
#    url,
#    headers=headers,
#    params=params
#  )
  logging.info(response.text)
  if response is not None:
    data = response.json()
    if response.status_code == 200:
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
