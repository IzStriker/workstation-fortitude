from workstationfortitude.vmnotfound import VMNotFound

import requests
import json
import os


def get_virtual_machines(credentials: str) -> str:
    headers = {
        "Accept" : "application/vnd.vmware.vmw.rest-v1+json",
        "Authorization" : "Basic " + credentials
    }
    res = requests.get("http://127.0.0.1:8697/api/vms", headers=headers)
    return json.loads(res.text)

def get_vm_id(name: str, credentials: str) -> str:
    for vm in get_virtual_machines(credentials):
        base = os.path.basename(vm["path"])
        if name == os.path.splitext(base)[0]:
            return vm["id"]
    raise VMNotFound(name)