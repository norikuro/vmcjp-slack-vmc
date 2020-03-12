
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
    message_handler(msg_const.SDDCS_TXT, event)
    event.update(
        {
#            "sddcs": list_sddcs_(
            "sddcs": sddc_list(
#                event.get("token"), 
                event.get("access_token"), 
                event.get("org_id")
            )
        }
    )
    message_handler(msg_const.SDDCS_MSG, event)
