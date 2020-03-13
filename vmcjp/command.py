import time
import logging

from vmcjp.slack.db import write_cred_db
from vmcjp.vmc.vmc_client import login, sddc_list

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event):
    logging.info(event)
    expire_time = event.get("expire_time")
    command = event.get("vmc_command")
    
    if "list_sddcs" in command:
        data = login(event.get("token"))
        event.update(data)
    else:
        if expire_time is not None and expired(expire_time):
            data = login(event.get("token"))
            event.update(data)
            write_cred_db(
                event.get("db_url"),
                event.get("user_id"),
                data
            )
    eval(event.get("vmc_command"))(event)

def expired(expire_time):
    now = time.time()
    return now > expire_time

def list_sddcs(event):
    return sddc_list(
        event.get("access_token"), 
        event.get("org_id")
    )
