
def event_handler(event):
    response = login(event.get("token"))
    if response is not None:
        event.update(
            {
                "access_token": response.get("access_token")
            }
        )    
    eval(cmd)(event, db)

def list_sddcs(event, db):
    return sddc_list(
        event.get("access_token"), 
        event.get("org_id")
    )
