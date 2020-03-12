from vmcjp.utils import msg_const, cmd_const
from vmcjp.utils.lambdautils import call_lambda
from vmcjp.utils.loginutils import validate_token
from vmcjp.slack.messages import message_handler
#from vmcjp.vmc.vmc_client import list_sddcs_, list_sddcs__, get_max_num_hosts, is_network, is_valid_network, check_sddc_user
from vmcjp.vmc.vmc_client import list_sddcs__, get_max_num_hosts, is_network, is_valid_network, check_sddc_user
from vmcjp.vmc.vmc_client2 import login, sddc_list, sddc_name_and_id_list

def command_handler(cmd, event, db):
    response = login(event.get("token"))
    if response is not None:
        event.update(
            {
                "access_token": response.get("access_token")
            }
        )    
    eval(cmd)(event, db)

def cancel_register(event, db):
    message_handler(msg_const.CANCEL_TOKEN, event)
    db.delete_cred_db(event.get("user_id"))

def register_org(event, db):
    message_handler(msg_const.REGISTER_ORG, event)
    db.write_cred_db(
        event.get("user_id"), 
        {
            "status": cmd_const.REGISTER_ORG_ID
        }
    )

def register_org_id(event, db):
    message_handler(msg_const.REGISTER_TOKEN, event)
    db.write_cred_db(
        event.get("user_id"), 
        {
            "org_id": event.get("text"),
            "status": cmd_const.REGISTER_TOKEN
        }
    )

def register_token(event, db):
    cred = db.read_cred_db(event.get("user_id"))
    user_name = validate_token(event.get("text"), cred.get("org_id"))
    if user_name is not None:
        message_handler(msg_const.SUCCESS_TOKEN, event)
        db.write_cred_db(
            event.get("user_id"), 
            {
                "status": cmd_const.REGISTERED, 
                "token": event.get("text"), 
                "user_name": user_name
            }
        )
    else:
        message_handler(msg_const.FAILED_TOKEN, event)
        message_handler(msg_const.WRONG_TOKEN, event)
        db.delete_cred_db(event.get("user_id"))

def delete_org(event, db):
    message_handler(msg_const.DELETE_ORG, event)
    db.delete_cred_db(event.get("user_id"))

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

def create_zero_sddc(event, db): #for internal test only
    message_handler(msg_const.SDDC_WIZARD, event)
    message_handler(msg_const.CHECK_RESOURCE, event)
    max_hosts = get_max_num_hosts(
        event.get("token"),
        event.get("org_id")
    )
    event.update({"max_hosts": max_hosts})
    if max_hosts < 1:
        message_handler(msg_const.NOT_ENOUGH, event)
        db.delete_event_db(event.get("user_id"))
    else:
        message_handler(msg_const.MAX_HOSTS, event)
        db.write_event_db(
            event.get("user_id"), 
            {
                "command": cmd_const.COMMAND_SDDC[event.get("text")],
                "status": cmd_const.CHECK_MAX_HOSTS, 
                "max_hosts": max_hosts,
                "provider": "ZEROCLOUD"
            }
        )

def create_sddc(event, db):
    message_handler(msg_const.SDDC_WIZARD, event)
    message_handler(msg_const.CHECK_RESOURCE, event)
    max_hosts = get_max_num_hosts(
        event.get("token"),
        event.get("org_id")
    )
    event.update({"max_hosts": max_hosts})
    if max_hosts < 1:
        message_handler(msg_const.NOT_ENOUGH, event)
        db.delete_event_db(event.get("user_id"))
    else:
        message_handler(msg_const.MAX_HOSTS, event)
        db.write_event_db(
            event.get("user_id"), 
            {
                "command": cmd_const.COMMAND_SDDC[event.get("text")],
                "status": cmd_const.CHECK_MAX_HOSTS, 
                "max_hosts": max_hosts,
                "provider": "AWS"
            }
        )

def delete_sddc(event, db):
    event.update(
        {
            "option_list": list_sddcs__(
                event.get("token"), 
                event.get("org_id")
            )
        }
    )
    message_handler(msg_const.DELETE_SDDC, event)
    db.write_event_db(
        event.get("user_id"),
        {
            "command": cmd_const.COMMAND_SDDC[event.get("text")],
            "status": cmd_const.DELETE_SDDC
        }
    )
    
def selected_sddc_to_delete(event, db):
    sddc_name = event.get("response").split("+")[0]
    sddc_id = event.get("response").split("+")[1]
    event.update(
        {"sddc_name": sddc_name}
    )
    db.write_event_db(
        event.get("user_id"),
        {
            "sddc_name": sddc_name,
            "sddc_id": sddc_id
        }
    )
    message_handler(msg_const.CONFIRM_DELETE, event)

def delete_confirmation(event, db):
    response = event.get("response")
    if "yes" in response:
        message_handler(msg_const.START_DELETE, event)
#        event.update(result)
        event.update(
            {"user_name": event.get("user_name")}
        )
        if check_sddc_user(
            event.get("token"),
            event.get("org_id"),
            event.get("sddc_id"),
            event.get("user_name")
        ):
            call_lambda("delete_sddc", event)
        else:
            message_handler(msg_const.CANT_DELETE, event)
            db.delete_event_db(event.get("user_id"))
    else:
        message_handler(msg_const.CANCEL_DELETE, event)
        db.delete_event_db(event.get("user_id"))

def restore_sddc(event, db): #for internal only
    hoge = 1

def sddc_name(event, db):
    if event.get("max_hosts") == 1:
        message_handler(msg_const.LINK_AWS, event)
        db.write_event_db(
            event.get("user_id"), 
            {
                "status": cmd_const.AWS_ACCOUNT, 
                "sddc_name": event.get("text")
            }
        )
    else:
        message_handler(msg_const.SINGLE_MULTI, event)
        db.write_event_db(
            event.get("user_id"), 
            {
                "status": cmd_const.SINGLE_MULTI, 
                "sddc_name": event.get("text")
            }
        )

def mgmt_cidr(event, db):
    text = event.get("text")
    
    if is_network(text):
        if is_valid_network(text):
            event.update({"vpc_cidr": text})
            message_handler(msg_const.SDDC_CONFIRM, event)
            db.write_event_db(
                event.get("user_id"), 
                {
                    "status": cmd_const.CHECK_CONFIG, 
                    "vpc_cidr": text
                }
            )
    else:
        message_handler(msg_const.WRONG_NETWORK, event)
