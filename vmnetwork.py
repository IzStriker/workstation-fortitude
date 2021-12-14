import requests
import json
import os
from workstationfortitude import BASE_URL, configutils, vmmanagement

from workstationfortitude.nointerfacesrequired import NoInterfacesRequired
from workstationfortitude.interfacecreationexception import InterfaceCreationException

def add_interfaces(vm_id: str, num_interfaces: int, credentials: str) -> int:
    headers = {
        "Accept" : "application/vnd.vmware.vmw.rest-v1+json",
        "Authorization" : "Basic " + credentials
    }
    res = json.loads(requests.get(f"{BASE_URL}/vms/{vm_id}/nic", headers=headers).text)

    num_interfaces -= res["num"]

    if num_interfaces < 1:
        raise NoInterfacesRequired()
    
    headers["Content-Type"] = "application/vnd.vmware.vmw.rest-v1+json"
    body = {
        "type": "nat"
    }
    for _ in range(num_interfaces):
        res = requests.post(f"{BASE_URL}/vms/{vm_id}/nic", headers=headers, json=body)
        if res.status_code != 201:
            raise InterfaceCreationException(res.text)
    return num_interfaces

def get_lan_segments():
    lan_segments = {}

    try:
        i = 0
        while True:
            name = configutils.get_option(f"pref.namedPVNs{i}.name", os.environ.get('appdata') + "\VMware\preferences.ini")
            lan_segments[name] = configutils.get_option(f"pref.namedPVNs{i}.pvnID", os.environ.get('appdata') + "\VMware\preferences.ini")
            i += 1
    except:
        pass    
    
    return lan_segments

def configure_interface_type(interfaces: list, vm_id: str, credentials: str):
    lan_segments = get_lan_segments()
    
    vm_path = vmmanagement.get_vm_path(vm_id, credentials)
    i = 0
    for interface in interfaces:
        if interface['type'] == "lan":
            configutils.set_option(f"ethernet{i}.connectionType", "pvn", vm_path)
            try:
                configutils.set_option(f"ethernet{i}.pvnID", lan_segments[interface['name']], vm_path)
            except:
                configutils.add_option(f"ethernet{i}.pvnID", lan_segments[interface['name']], vm_path)
        i += 1
