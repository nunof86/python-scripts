#Compare powerdns IPs with netbox IPs (compare the json file with the CSV file from netbox)
#Write a CSV file with the format (x.x.x.x/x) with IPs to remove from netbox
#Change the JSON and CSV files to match your needs

import ipaddress
import json
import csv

with open('Name of the file.json', 'r') as powerdns_file:
    powerdns_data = json.load(powerdns_file)

netbox_ips = set()
ips_to_keep = {'x.x.x.x'}
networks_to_keep = {'x.x.x.x'}

with open('Name of the netbox csv file', 'r') as netbox_file:
    csv_reader = csv.DictReader(netbox_file)
    for row in csv_reader:
        ip_with_mask = row['IP Address']
        netbox_ips.add(ip_with_mask)

ips_to_remove = set()

for ip_with_mask in netbox_ips:
    ip_interface = ipaddress.ip_interface(ip_with_mask)
    ip_address = ip_interface.ip

    in_powerdns = str(ip_address) in powerdns_data
    in_ips_to_keep = any(ipaddress.ip_address(ip) == ip_address 
                         for ip in ips_to_keep)
    in_networks_to_keep = any(ip_interface.network.overlaps(ipaddress.ip_network(ip)) 
                              for ip in networks_to_keep)

    if not in_powerdns and not in_ips_to_keep and not in_networks_to_keep:
        ips_to_remove.add(str(ip_interface))

with open('Name of the file', 'w', newline='') as output_file:
    fieldnames = ['address']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    for ip in ips_to_remove:
        writer.writerow({'address': ip})