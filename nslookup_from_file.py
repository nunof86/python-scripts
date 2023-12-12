#Nslookp from a file
#Change the csv_filename to match the loacation and the name of the CSV file that is opened
#Change the output_csv_filename to match the loacation and the name of the CSV file that is created
#Need to have the csv_filename with a row named IP
import csv
import socket

results = []

csv_filename = 'ips_not_in_netbox.csv'
output_csv_filename = 'nslookup_results.csv'

with open(csv_filename, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        ip = row['IP']
        try:
            host = socket.gethostbyaddr(ip)
            results.append({'IP': ip, 'DNS Name': host[0]})
        except socket.herror:
            results.append({'IP': ip, 'DNS Name': 'Not found'})

with open(output_csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['IP', 'DNS Name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        writer.writerow(result)

print(f'Results saved in {output_csv_filename}')
