import time
#import logging

from vmcjp.utils import cmd_const
from vmcjp.slack.db import write_cred_db
from vmcjp.vmc.vmc_client import login, sddc_list, token_validation, get_sddcs, get_sddclimit, get_aws_region, get_connected_accounts

#logger = logging.getLogger()
#logger.setLevel(logging.INFO)

def lambda_handler(event, context):
#    logging.info(event)
    expire_time = event.get("expire_time")
    command = event.get("vmc_command")
    
    if expire_time is None and command != "validate_token":
        data = login(event.get("token"))
        event.update(data)
        write_cred_db(
            event.get("db_url"),
            event.get("user_id"),
            data
        )
    elif expire_time is not None and expired(expire_time):
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

def validate_token(event):
    return token_validation(
        event.get("token"),
        event.get("org_id")
    )

def list_sddcs(event):
#    list = sddc_list(
#        event.get("access_token"), 
#        event.get("org_id")
#    )
    return sddc_list(
        event.get("access_token"), 
        event.get("org_id")
    )
#    return list

def check_max_hosts(event):
    sddclimit = get_sddclimit(
        event.get("access_token"), 
        event.get("org_id")
    )
    sddcs = get_sddcs(
        event.get("access_token"), 
        event.get("org_id")
    )
    
    i = 0
    for sddc in sddcs:
        i += len(sddc.get("resource_config").get("esx_hosts"))
    
    max_hosts = (sddclimit - 1) - i
#    if max_hosts < 1:
#        return max_hosts
#    else:
#        return 1 if max_hosts < 3 else max_hosts
    return 4 #for test

def list_region(event):
    regions = get_aws_region(
        event.get("access_token"), 
        event.get("org_id")
    )
    
    return [
        {
            "text": region,
            "value": region
        } for region in regions
    ]

def list_aws_account(event):
    accounts = get_connected_accounts(
        event.get("access_token"), 
        event.get("org_id")
    )
    
    if accounts is not None:
        return [
            {
                "text": account.get("account_number"),
                "value": "{}+{}".format(
                    account.get("account_number"), 
                    account.get("id")
                )
            } for account in accounts
        ]

def list_vpc(event):
    return [
        {
            "text": vpc,
            "value": vpc
        } for vpc in vpcs
    ]
