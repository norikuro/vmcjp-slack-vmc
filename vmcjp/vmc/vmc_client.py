import json
import time
#import logging

from vmcjp.utils.vmc_restutils import post_request, get_request

LOGIN_URL = "https://console.cloud.vmware.com/csp/gateway"
VMC_URL = "https://vmc.vmware.com/vmc/api"
HEADERS = {"Content-Type": "application/json"}

#logger = logging.getLogger()
#logger.setLevel(logging.INFO)

def update_headers(access_token):
    headers = {"csp-auth-token": access_token}
    headers.update(HEADERS)
    return headers

def login(refresh_token):
    uri = "/am/api/auth/api-tokens/authorize"
    query = {"refresh_token": refresh_token}
    
    data = post_request(
        '{}{}'.format(LOGIN_URL, uri),
        HEADERS,
        query=query
    )
    now = time.time()
    
    if data.get("error_messages") is None:
        return {
            "access_token": data.get("access_token"),
            "expire_time": now + data.get("expires_in") - 180 # minus 3 minutes for extra time befire expire the access_token
        }
    else:
        return data

def get_org_id_by_token(refresh_token):
    uri = "/am/api/auth/api-tokens/details"
    
    data = post_request(
        '{}{}'.format(LOGIN_URL, uri),
        HEADERS,
        params={"tokenValue": refresh_token}
    )
    
    return data

def token_validation(refresh_token, org_id):
    data = get_org_id_by_token(refresh_token)
    
    if data.get("error_messages") is None:
        if data.get("orgId") == org_id:
            return data.get("username")
    else:
        return data

def get_sddcs(access_token, org_id):
    uri = "/orgs/{}/sddcs".format(org_id)
#    headers = {"csp-auth-token": access_token}
#    headers.update(HEADERS)
    
    data = get_request(
        '{}{}'.format(VMC_URL, uri),
#        headers
        update_headers(access_token)
    )
    
    return data

def sddc_name_and_id_list(access_token, org_id):
    sddcs = get_sddcs(access_token, org_id)
    if data.get("error_messages") is None:
        #return list
        return [
            {
                "text": sddc.get("name"),
                "value": "{}+{}".format(
                    sddc.get("name"), 
                    sddc.get("resource_config").get("sddc_id")
                )
            } for sddc in sddcs
        ]
    else:
        return data

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

def get_org(access_token, org_id):
    uri = "/orgs/{}".format(org_id)
    
    data = get_request(
        '{}{}'.format(VMC_URL, uri),
        update_headers(access_token)
    )
    
    return data

def get_sddclimit(access_token, org_id):
    data = get_org(access_token, org_id)
    
    if data.get("error_messages") is None:
        return int(data.get("properties").get("values").get("sddcLimit"))
    else:
        return data

def get_aws_region(access_token, org_id):
    uri = "/orgs/{}/sddcs/provision-spec".format(org_id)
#    data = get_org(access_token, org_id)
    
    data = get_request(
        '{}{}'.format(VMC_URL, uri),
        update_headers(access_token)
    )
    
    if data.get("error_messages") is None:
#        return data.get("properties").get("values").get("defaultAwsRegions").split(",")
        return data.get("provider").get("AWS").get("region_display_names")
    else:
        return data

def get_connected_accounts(access_token, org_id):
    uri = "/orgs/{}/account-link/connected-accounts".format(org_id)
    
    data = get_request(
        '{}{}'.format(VMC_URL, uri),
        update_headers(access_token)
    )
    
    return data

def get_vpc_map(access_token, org_id, linked_account_id, region):
    uri = "/orgs/{}/account-link/compatible-subnets".format(org_id)
    params = {"linkedAccountId": linked_account_id, "region": region}
    
    data = get_request(
        '{}{}'.format(VMC_URL, uri),
        update_headers(access_token),
        params = params
    )
    
    return data

def create_sddc(
    access_token, 
    org_id, 
    link_aws, 
    connected_account_id=None, 
    customer_subnet_id=None, 
    deployment_type=None, 
    host_instance_type=None, 
    sddc_name, 
    num_hosts, 
    provider, 
    region, 
    sddc_type=None, 
    size, 
    storage_capacity=None, 
    vpc_cidr
):
    uri = "/orgs/{}/sddcs".format(org_id)
    
    params = {
        "account_link_config": account_link_config(link_aws),
        "account_link_sddc_config": account_link_sddc_config(
            connected_account_id, 
            customer_subnet_id
        ) if link_aws else None,
        "deployment_type": deployment_type,
        "host_instance_type": host_instance_type,
        "name": sddc_name,
        "num_hosts": num_hosts,
        "one_node_reduced_capacity": false,
        "provider": provider,
        "region": region,
        "sddc_type": sddc_type,
        "size": size,
        "skip_creating_vxlan": False,
        "storage_capacity": storage_capacity,
        "vpc_cidr": vpc_cidr
    }
    
    data = post_request(
        '{}{}'.format(VMC_URL, uri),
        update_headers(access_token),
        params = params
    )
    
    return data

def account_link_config(link_aws):
    if link_aws:
        return {
            "delay_account_link": True
        }
    else:
        return {
            "delay_account_link": False
        }

def account_link_sddc_config(connected_account_id, customer_subnet_id):
    return [
        {
            "connected_account_id": connected_account_id,
            "customer_subnet_ids": 
            [
                customer_subnet_id
            ]
        }
    ]
