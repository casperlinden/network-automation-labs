import requests
from getpass import getpass
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = "10.10.20.48"
username = "developer"
password = getpass("Password: ")

url = f"https://{host}/restconf/data/ietf-interfaces:interfaces"

headers = {
    "Accept": "application/yang-data+json"
}

response = requests.get(
    url,
    headers=headers,
    auth=(username, password),
    verify=False
)

print(f"\nHTTP status: {response.status_code}")

if response.status_code == 200:
    data = response.json()

    print("\n--- INTERFACES ---")

    interfaces = data["ietf-interfaces:interfaces"]["interface"]

    for interface in interfaces:
        print(interface["name"])
else:
    print(response.text)