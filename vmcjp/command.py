import time

from vmcjp.slack.db import write_cred_db
from vmcjp.vmc.vmc_client import login, sddc_list

def lambda_handler(event):
    expire_time = event.get("expire_time")
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
