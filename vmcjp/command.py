import time
#import logging

from vmcjp.utils import cmd_const
from vmcjp.slack.db import write_cred_db
from vmcjp.vmc.vmc_client import login, sddc_list

#logger = logging.getLogger()
#logger.setLevel(logging.INFO)

def lambda_handler(event, context):
#    logging.info(event)
    expire_time = event.get("expire_time")
    command = event.get("vmc_command")
    
    if expire_time is None and command in cmd_const.COMMAND_SDDC:
        data = login(event.get("token"))
        write_cred_db(
            event.get("db_url"),
            event.get("user_id"),
            data
        )
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
    return eval(event.get("vmc_command"))(event)

def expired(expire_time):
    now = time.time()
    return now > expire_time

def list_sddcs(event):
    list = sddc_list(
        event.get("access_token"), 
        event.get("org_id")
    )
    return list
