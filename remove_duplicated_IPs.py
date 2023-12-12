#Remove the duplicated IPs from a CSV file
#Change the input_csv to match the loacation and the name of the CSV file that is opened
#Change the output_csv to match the loacation and the name of the CSV file that is created
import csv

input_csv = 'powerdns_ips.csv'
output_csv = 'unique_powerdns_ips.csv'

with open(input_csv, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    unique_ips = set()
    unique_rows = []
    
    for row in csv_reader:
        if len(row) > 0 and row[0].strip():
            ip = row[0].strip()
            
            if ip not in unique_ips:
                unique_ips.add(ip)
                unique_rows.append(row)

with open(output_csv, 'w', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    
    for row in unique_rows:
        csv_writer.writerow(row)

print(f'Removed duplicate lines and created the output file: {output_csv}')