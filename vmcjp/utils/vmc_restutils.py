import requests
import json
#import logging

#logger = logging.getLogger()
#logger.setLevel(logging.INFO)

def post_request(url, headers, params=None, data=None):
    if data is not None:
        data = json.dumps(data).encode("utf-8")
        
    try:
        response = requests.post(
            url,
            headers=headers,
            params=params,
            data=data
        )
        
    except requests.RequestException as e:
        raise Exception("Network error has occurred!")
        
    else:
        status = response.status_code
        resp_data = response.json()
        
    if status in [200, 202]:
        return resp_data
    elif status in [400, 401, 403, 404]:
        message = resp_data.get("message")
        error_messages = resp_data.get("error_messages")
        
        if message is not None:
#            logging.info("rest error has happened, {}".format(resp_data))
            raise Exception(message)
        elif error_messages is not None:
#            logging.info("rest error has happened, {}".format(resp_data))
            raise Exception(error_messages[0])
        else:
#            logging.info("rest error has happened, {}".format(resp_data))
            raise Exception("Something wrong!")
    else:
#        logging.info("rest error has happened, {}".format(resp_data))
        raise Exception("Something wrong!")
    
def get_request(url, headers, params=None):
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params
        )
    except requests.RequestException as e:
        raise Exception("Network error has occurred!")
        
    else:
        status = response.status_code
        resp_data = response.json()
        
        if status in [200, 202]:
            return resp_data
        elif status in [400, 401, 403, 404]:
            message = resp_data.get("message")
            error_messages = resp_data.get("error_messages")
            
            if message is not None:
                raise Exception(message)
            elif error_messages is not None:
                raise Exception(error_messages[0])
            else:
                raise Exception("Something wrong!")
        else:
            raise Exception("Something wrong!")

def delete_request(url, headers):
    try:
        response = requests.delete(
            url,
            headers=headers
        )
#        logging.info("!!! delete response: {}".format(response))
#        logging.info("!!! delete response: {}".format(response.json()))
        
    except requests.RequestException as e:
        raise Exception("Network error has occurred!")
        
    else:
        status = response.status_code
        resp_data = response.json()
        
    if status in [200, 202]:
        return resp_data
    elif status in [400, 401, 403, 404]:
        message = resp_data.get("message")
        error_messages = resp_data.get("error_messages")
        
        if message is not None:
            raise Exception(message)
        elif error_messages is not None:
            raise Exception(error_messages[0])
        else:
            raise Exception("Something wrong!")
    else:
        raise Exception("Something wrong!")
