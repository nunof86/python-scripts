#Remover IPs com base num csv (ips_to_remove)
import requests
import urllib3
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

def remove_ip_address(ip_id):
    try:
        response = requests.delete(NETBOX_URL + f'ipam/ip-addresses/{ip_id}/', 
                                   headers=headers, verify=False)
        response.raise_for_status()

        if response.status_code == 204:
            print(f"IP removed: {ip_id}")
        else:
            print(f"Error while removing: {ip_id}")
    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.RequestException as e:
        print(f"Request exception: {e}")


with open('Name of the file', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        ip_address_to_remove = row['address']
        ip_id_to_remove = get_ip_id_by_address(ip_address_to_remove)

        if ip_id_to_remove:
            print(f"Removing IP with ID: {ip_id_to_remove}")
            remove_ip_address(ip_id_to_remove)
        else:
            print(f"IP '{ip_address_to_remove}' not found in netbox.")
