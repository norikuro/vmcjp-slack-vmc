
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
    return sddc_list(
        event.get("token"), 
        event.get("org_id")
    )
