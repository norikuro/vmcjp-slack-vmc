
def event_handler(event):
    response = login(event.get("token"))
    if response is not None:
        event.update(
            {
                "access_token": response.get("access_token")
            }
        )    
    eval(event.get("vmc_command"))(event)

def list_sddcs(event):
    if check_access_token(
        event.get("expire_time")
    ):
        sddcs = {
            "sddc_list": sddc_list(
                event.get("access_token"), 
                event.get("org_id")
            )
        }
    else:
        access_token = login(event.get("token")
        sddcs = {
            "sddc_list": sddc_list(
                access_token, 
                event.get("org_id")
            )
        }
        sddcs.update(
            {
                "access_token": access_token
        )
    return sddcs
