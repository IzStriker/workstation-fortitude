from workstationfortitude.vmnotfound import VMNotFound

import requests
import json
import os

base_url = "http://127.0.0.1:8697"

def get_virtual_machines(credentials: str) -> str:
    headers = {
        "Accept" : "application/vnd.vmware.vmw.rest-v1+json",
        "Authorization" : "Basic " + credentials
    }
    res = requests.get(base_url + "/api/vms", headers=headers)
    return json.loads(res.text)

def get_vm_id(name: str, credentials: str) -> str:
    for vm in get_virtual_machines(credentials):
        base = os.path.basename(vm["path"])
        if name == os.path.splitext(base)[0]:
            return vm["id"]
    raise VMNotFound(name)

def clone_vm(name: str, parent_id: str, credentials: str) -> str:
    headers = {
      "Content-Type" : "application/vnd.vmware.vmw.rest-v1+json",
      "Accept" : "application/vnd.vmware.vmw.rest-v1+json",
      "Authorization" : "Basic " + credentials
    }

    body = {
        "name" : name,
        "parentId" : parent_id
    }

    res = requests.post(base_url + "/api/vms", headers=headers, json=body)
    
    return json.loads(res.text)