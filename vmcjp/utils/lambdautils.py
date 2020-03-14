import json
import logging

from botocore.session import Session
from botocore.config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def call_lambda(function, data):
    s = Session()
    clientLambda = s.create_client(
        "lambda", 
        config=Config(retries={'max_attempts': 0})
    )
    clientLambda.invoke(
        FunctionName=function,
        InvocationType="Event",
        Payload=json.dumps(data)
    )

def call_lambda_async(function, data):
    logging.info("!!!call_lambda: {}, {}".format(function, data))
    s = Session()
    clientLambda = s.create_client(
        "lambda", 
        config=Config(retries={'max_attempts': 0})
    )
    clientLambda.invoke(
        FunctionName=function,
        InvocationType="Event",
        Payload=json.dumps(data)
    )

def call_lambda_sync(function, data):
    s = Session()
    clientLambda = s.create_client(
        "lambda", 
        config=Config(retries={'max_attempts': 0})
    )
    response = clientLambda.invoke(
        FunctionName=function,
        InvocationType="RequestResponse",
        Payload=json.dumps(data)
    )
    body = json.loads(response['Payload'].read())
    return body
