import json
import time
#import logging

from vmcjp.utils.vmc_restutils import post_request, get_request

LOGIN_URL = "https://console.cloud.vmware.com/csp/gateway"
VMC_URL = "https://vmc.vmware.com/vmc/api"
HEADERS = {"Content-Type": "application/json"}

#logger = logging.getLogger()
#logger.setLevel(logging.INFO)

def login(refresh_token):
    uri = "/am/api/auth/api-tokens/authorize"
    query = {"refresh_token": refresh_token}
    
    data = post_request(
        '{}{}'.format(LOGIN_URL, uri),
        HEADERS,
        query=query
    )
    now = time.time()
    
    if data is not None:
        return {
            "access_token": data.get("access_token"),
            "expire_time": now + data.get("expires_in") - 180 # minus 3 minutes for extra time befire expire the access_token
        }

def get_org_id_by_token(refresh_token, org_id):
    uri = "/am/api/auth/api-tokens/details"
    
    data = post_request(
        '{}{}'.format(LOGIN_URL, uri),
        HEADERS
    )

def get_sddcs(access_token, org_id):
    uri = "/orgs/{}/sddcs".format(org_id)
    headers = {"csp-auth-token": access_token}
    headers.update(HEADERS)
    
    data = get_request(
        '{}{}'.format(VMC_URL, uri),
        headers
        
    )
    if data is not None:
        return data

def sddc_name_and_id_list(access_token, org_id):
    sddcs = get_sddcs(access_token, org_id)
    if sddcs is not None:
        return [
            {
                "text": sddc.get("name"),
                "value": "{}+{}".format(
                    sddc.get("name"), 
                    sddc.get("resource_config").get("sddc_id")
                )
            } for sddc in sddcs
        ]

def sddc_list(access_token, org_id):
    sddcs = get_sddcs(access_token, org_id)
    if sddcs is not None:
        return [
            {
                "sddc_name": sddc.get("name"),
                "user_name": sddc.get("user_name"),
                "created": sddc.get("created"),
                "num_hosts": len(sddc.get("resource_config").get("esx_hosts"))
            } for sddc in sddcs
        ]
