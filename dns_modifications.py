#Compare the differences between the DNS name of the IPs in the netbox with the data from PowerDNS and save in a CSV file
#Change the names of the CSV files(file of netbox IPs and a CSV filewith only A records)

import csv
import socket

netbox_data = {}
modifications = []

with open('Name of the file', 'r') as netbox_file:
    csv_reader = csv.DictReader(netbox_file)
    for row in csv_reader:
        ip_with_mask = row['IP Address']
        dns_name = row['DNS name']
        netbox_data[ip_with_mask] = dns_name

with open('Name of the file', 'r') as ips_file:
    csv_reader = csv.DictReader(ips_file)
    for row in csv_reader:
        ip = row['IP']
        ip_found = False
        for netbox_ip in netbox_data:
            netbox_ip_network = netbox_ip.split('/')[0]
            if ip == netbox_ip_network:
                ip_found = True
                expected_dns_name = netbox_data[netbox_ip]
                try:
                    host = socket.gethostbyaddr(ip)
                    dns_name = host[0]
                    if dns_name != expected_dns_name:
                        if not any(mod['address'] == netbox_ip for mod in 
                                   modifications):
                            modifications.append({
                                'address': netbox_ip,
                                'netbox_dns_name': expected_dns_name,
                                'dns_name': dns_name
                            })
                except socket.herror:
                    continue

if modifications:
    with open('Name of the file', 'w', newline='') as csv_file:
        fieldnames = ['address', 'netbox_dns_name', 'dns_name']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(modifications)
        print('Modifications saved.')
else:
    print('No modifications detected.')