#DNS query of the specified network from a JSON file generated in the get_info script and append the information of the json file(comments)
#Change the csvfile to match the loacation and the name of the CSV file that is created
#Change the json_file to match the loacation and the name of the JSON file that is opened
#Change the subnet and the prefix_length to match the network and netmask of the required network
import dns.resolver
import csv
import ipaddress
import json

def dns_query(subnet, prefix_length):

    network = ipaddress.IPv4Network(f'{subnet}/{prefix_length}', strict=False)
    

    with open("powerdns_descriptions.json", "r") as json_file:
        descriptions = json.load(json_file)
    

    with open(f'network{subnet}_{prefix_length}.csv', 'w', newline='') as csvfile:
        fieldnames = ['address', 'status', 'dns_name', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
 
        writer.writeheader()
        
        for ip in network.hosts():
            try:
                host = dns.resolver.resolve(ip.reverse_pointer, 'PTR')
                for result in host:
                    dns_name = str(result).rstrip('.')
                    description = descriptions.get(str(ip), "")
                    writer.writerow({'address': f'{ip}/{prefix_length}', 'status': 'active', 'dns_name': dns_name, 'description': description})
            except dns.resolver.NXDOMAIN:
                pass

subnet = 'YOUR NETWORK IP'
prefix_length = 24
dns_query(subnet, prefix_length)
