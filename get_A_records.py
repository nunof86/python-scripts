#Get all PowerDNS A records
#Change the POWERDNS_URL to match your API URL
#Change the POWERDNS_API_TOKEN to match your API TOKEN
#Change the csv_filename to match the loacation and the name of the CSV file that is created
import requests
import csv

POWERDNS_URL = "YOUR API"
POWERDNS_API_TOKEN = "YOUR API TOKEN"

def fetch_dns_records():
    headers = {"X-API-Key": POWERDNS_API_TOKEN}
    response = requests.get(f"{POWERDNS_URL}/zones", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error. CODE: {response.status_code}")
        return []

def extract_a_records(zone_data):
    a_records = []
    zone_id = zone_data["id"]
    headers = {"X-API-Key": POWERDNS_API_TOKEN}
    response = requests.get(f"{POWERDNS_URL}/zones/{zone_id}", headers=headers)
    if response.status_code == 200:
        zone_details = response.json()
        for record in zone_details["rrsets"]:
            if record["type"] == "A":
                for item in record["records"]:
                    a_records.append(item["content"])
    return a_records

def write_dns_records_to_csv(records, csv_filename):
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["IP"])
        for record in records:
            csv_writer.writerow([record])

def main():
    dns_records = fetch_dns_records()
    if dns_records:
        a_records = []
        for zone in dns_records:
            a_records.extend(extract_a_records(zone))
        
        csv_filename = "powerdns_ips.csv"
        write_dns_records_to_csv(a_records, csv_filename)
        print(f"Info saved in {csv_filename}")

if __name__ == "__main__":
    main()
