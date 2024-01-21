#Change the DNS name of the netbox IP based on a CSV file
#Change the CSV file to match your needs

import requests
import urllib3
import json
import csv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NETBOX_URL = 'YOUR API'
API_TOKEN = 'YOUR API TOKEN'

headers = {
    'Authorization': f'Token {API_TOKEN}',
    'Content-Type': 'application/json',
}

def get_ip_id_by_address(address):
    try:
        response = requests.get(NETBOX_URL + f'ipam/ip-addresses/?address={address}', 
                                headers=headers, verify=False)
        response.raise_for_status()
        response_data = response.json()

        if response_data['count'] > 0:
            return response_data['results'][0]['id']
    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.RequestException as e:
        print(f"Request exception: {e}")

    return None

def update_ip_address(ip_id, dns_name):
    data = {
        'dns_name': dns_name,
    }

    try:
        response = requests.patch(NETBOX_URL + f'ipam/ip-addresses/{ip_id}/', 
                                  headers=headers, data=json.dumps(data), 
                                  verify=False)
        response.raise_for_status()

        if response.status_code == 200:
            print("DNS updated.")
        else:
            print(f"Error while changing DNS: {response.text}")
    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.RequestException as e:
        print(f"Request exception: {e}")

with open('Name of the file', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        ip_address_to_update = row['address']
        new_dns_name = row['dns_name']

        ip_id_to_update = get_ip_id_by_address(ip_address_to_update)

        if ip_id_to_update:
            print(f"IP found, ID: {ip_id_to_update}")
            update_ip_address(ip_id_to_update, new_dns_name)
        else:
            print(f"IP '{ip_address_to_update}' not found.")
