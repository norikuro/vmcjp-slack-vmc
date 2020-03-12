from vmcjp.slack.db import write_cred_db

def lambda_handler(event):
    if expired(event.get("expire_time")):
        event.update(
            {
                "access_token": response.get("access_token")
            }
        )
        
    eval(event.get("vmc_command"))(event)

def list_sddcs(event):
    return sddc_list(
        event.get("access_token"), 
        event.get("org_id")
    )
