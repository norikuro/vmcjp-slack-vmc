import requests
import json

def post_request(url, headers, params):
  response = requests.post(
    url,
    headers=headers,
    params=params
  )
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
