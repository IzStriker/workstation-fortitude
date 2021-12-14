import requests
import json
import os
from workstationfortitude import BASE_URL, configutils

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

def get_lan_segments(interfaces: list):
    lan_segments = {}


    for interface in interfaces:
        if(interface['type'] == 'lan'):
            lan_segments[interface['name']] = configutils.get_option("pref.namedPVNs\\d.pvnID", os.environ.get('appdata') + "\VMware\preferences.ini")
    
    return lan_segments

def configure_interface_type(interfaces: list):
    print(get_lan_segments(interfaces))
    # Check all lan segements exist 
    # If interface face type isn't nat convert to lan segment