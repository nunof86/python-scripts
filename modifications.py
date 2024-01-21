#See the differences between nebox and powerdns based on the first octets of the networks
#Change the firts octects to match your needs
#Change the name of the CSV files created to match your needs
#IPs that are not in the netbox, do nslookup and save in a file

import csv
import json
import socket

netbox_data = {}
with open('Name of the file', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        ip_with_mask = row['IP Address']
        description = row['Description']

        ip = ip_with_mask.split('/')[0]

        netbox_data[ip] = description

with open('Name of the file', 'r') as json_file:
    powerdns_data = json.load(json_file)

modifications = []
ips_not_in_powerdns = []
ips_not_in_netbox = []

def is_desired_octet(ip):
    first_octet = int(ip.split('.')[0])
    return first_octet in [10, 172, 193, 194]

for ip, netbox_description in netbox_data.items():
    if ip in powerdns_data:
        powerdns_description = powerdns_data[ip]
        if powerdns_description != netbox_description:
            modifications.append({
                'address': ip,
                'description': powerdns_description,
                'netbox_description': netbox_description
            })
    else:
        if is_desired_octet(ip):
            ips_not_in_powerdns.append(ip)

for ip in powerdns_data:
    if ip not in netbox_data:
        if is_desired_octet(ip):
            ips_not_in_netbox.append(ip)

with open('Name of the file', 'w', newline='') as csv_file:
    fieldnames = ['address', 'description', 'netbox_description']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(modifications)

with open('Name of the file', 'w', newline='') as csv_file:
    fieldnames = ['IP']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([{'IP': ip} for ip in ips_not_in_powerdns])

with open('Name of the file', 'w', newline='') as csv_file:
    fieldnames = ['IP']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([{'IP': ip} for ip in ips_not_in_netbox])


resultados = []

csv_filename = 'Name of the file'

with open(csv_filename, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        ip = row['IP']
        try:
            host = socket.gethostbyaddr(ip)
            resultados.append({'IP': ip, 'DNS Name': host[0]})
        except socket.herror:
            resultados.append({'IP': ip, 'DNS Name': 'Not Found'})

with open('Name of the file', 'w', newline='') as csvfile:
    fieldnames = ['IP', 'DNS Name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for resultado in resultados:
        writer.writerow(resultado)