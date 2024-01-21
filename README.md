# python-scripts
Python Scripts for a wide variety of purposes

## List of scripts



### `A_records+comments`

Get all PowerDNS A records and comments and save in a CSV file

### `dns_from_network`

DNS query of the specified network from a JSON file generated in the `get_info` script and append the information of the json file(comments)

### `get_A_records`

Get all PowerDNS A records

### `get_info`

Get all PowerDNS A records and comments and saved in a JSON file

### `nslookup_from_file`

Nslookp from a file

### `remove_duplicated_IPs`

Remove the duplicated IPs from a CSV file

### `different_ips`

Compare powerdns IPs with netbox IPs and write them in a CSV file

### `removing_ips`

Remove IPs based on the CSV file from the `different_ips` script

### `dns_modifications`

Compare the differences between the DNS of the PowerDNS and netbox and write them in a CSV file


### `modificar_dns`

Change the DNS name of the netbox IP based on a CSV file from the `dns_modifications` script

### `modifications`

See the differences between nebox and powerdns based on the first octets of the networks and write them in a CSV file

### `change_descriptions`

Change netbox descriptions based on a CSV file from the `modifications` script
