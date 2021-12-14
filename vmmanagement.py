from workstationfortitude import BASE_URL
from workstationfortitude.vmnotfound import VMNotFound
import subprocess
import requests
import json
import os


def get_virtual_machines(credentials: str) -> dict:
    headers = {
        "Accept" : "application/vnd.vmware.vmw.rest-v1+json",
        "Authorization" : "Basic " + credentials
    }
    res = requests.get(f"{BASE_URL}/vms", headers=headers)
    return json.loads(res.text)

def get_vm_path(id: str, credentials: str) -> str:
    for vm in get_virtual_machines(credentials):
        if vm["id"] == id:
            return vm["path"]
    raise VMNotFound

def get_vm_id(name: str, credentials: str) -> str:
    for vm in get_virtual_machines(credentials):
        base = os.path.basename(vm["path"])
        if name == os.path.splitext(base)[0]:
            return vm["id"]
    raise VMNotFound(name)

def get_vm_info(id: str, credentials: str) -> str:
    headers = {
        "Accept" : "application/vnd.vmware.vmw.rest-v1+json",
        "Authorization" : "Basic " + credentials
    }
    res = requests.get(f"{BASE_URL}/vms/{id}", headers=headers)
    return json.loads(res.text)

def clone_vm(name: str, parent_id: str, credentials: str) -> dict:
    headers = {
      "Content-Type" : "application/vnd.vmware.vmw.rest-v1+json",
      "Accept" : "application/vnd.vmware.vmw.rest-v1+json",
      "Authorization" : "Basic " + credentials
    }

    body = {
        "name" : name,
        "parentId" : parent_id
    }

    res = requests.post(f"{BASE_URL}/vms", headers=headers, json=body)
    
    return json.loads(res.text)

def linked_clone_vm(name: str, parent_id: str, credentials: str) -> dict:
    vmrun_path = os.path.join(os.environ.get('PROGRAMFILES(X86)'), "VMware\\VMware Workstation\\")
    parent_path = get_vm_path(parent_id, credentials)
    vm_library = os.path.dirname(os.path.dirname(parent_path))
    vm_path = os.path.join(vm_library, name, name + ".vmx")
    
    args = ["vmrun.exe", "clone", parent_path, vm_path, "linked"]

    subprocess.call(args, shell=True, cwd=vmrun_path)
    
    id = get_vm_id(name, credentials)
    return get_vm_info(id, credentials)

def register_vm(id: str, name: str, credentials: str):
    headers = {
        "Content-Type" : "application/vnd.vmware.vmw.rest-v1+json",
        "Accept" : "application/vnd.vmware.vmw.rest-v1+json",
        "Authorization" : "Basic " + credentials
    }
    body = {
        "name" : name,
        "path" : get_vm_path(id, credentials)
    }

    res = requests.post(f"{BASE_URL}/vms/registration", headers=headers, json=body)
    return json.loads(res.text)