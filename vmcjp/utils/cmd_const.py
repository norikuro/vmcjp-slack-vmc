#!/usr/bin/env python

import sys

class _const:
  #followings are command names which we can do on slack app
  REGISTER_ORG = "register_org"
  DELETE_ORG = "delete_org"
  CREATE_ZEROCLOUD_SDDC = "create_zero_sddc"
  CREATE_SDDC = "create_sddc"
  DELETE_SDDC = "delete_sddc"
  LIST_SDDCS = "list_sddcs"
  RESTORE_SDDC = "restore_sddc" # for internal use
  
  COMMAND_ORG = {
#    "register org": "register_org",
#    "delete org": "delete_org"
    "register org": REGISTER_ORG,
    "delete org": DELETE_ORG
  }
  
  COMMAND_SDDC = {
    "create zerocloud sddc": "create_zero_sddc",
    "create sddc": "create_sddc",
    "delete sddc": "delete_sddc",
    "list sddcs": "list_sddcs",
    "restore sddc": "restore_sddc", # for internal use
  }
  
  #followings are status of register ORG and token
  REGISTER_ORG_ID = "register_org_id"
  REGISTER_TOKEN = "register_token"
  REGISTERED = "registered"
  CANCEL_REGISTER = "cancel_register"
  
  #followings are status of create SDDC
  CHECK_MAX_HOSTS = "check_max_hosts"
  AWS_REGION = "aws_region"
  SDDC_NAME = "sddc_name"
  SINGLE_MULTI = "single_multi"
  NUM_HOSTS = "num_hosts"
  AWS_ACCOUNT = "aws_account"
  AWS_VPC = "aws_vpc"
  AWS_SUBNET = "aws_subnet"
  MGMT_CIDR = "mgmt_cidr"
  CHECK_CONFIG = "check_config"
  CREATING = "creating"
  
  #followings are status of delete SDDC
  DELETE_SDDC = "delete_sddc"

  class ConstError(TypeError):
    pass
  
  def __setattr__(self, name, value):
    if name in self.__dict__:
      raise self.ConstError("Can't rebind const (%s)" % name)
    self.__dict__[name] = value

sys.modules[__name__]=_const()
