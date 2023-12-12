#Get all PowerDNS A records and comments and saved in a JSON file
#Change the POWERDNS_URL to match your API URL
#Change the POWERDNS_API_TOKEN to match your API TOKEN
#Change the csv_filename to match the loacation and the name of the CSV file that is created
import requests
import json

POWERDNS_URL = "YOUR API HERE"
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
                    ip = item["content"]
                    description = ", ".join(comment["content"] for comment in record.get("comments", []))
                    a_records.append({"IP": ip, "Description": description})
        return a_records

def save_descriptions_to_json(descriptions, json_filename):
    with open(json_filename, "w") as json_file:
        json.dump(descriptions, json_file)
    print(f"Information saved in '{json_filename}'")

def main():
    dns_records = fetch_dns_records()
    if dns_records:
        a_records = []
        descriptions = {}
        for zone in dns_records:
            records = extract_a_records(zone)
            a_records.extend(records)
            for record in records:
                descriptions[record["IP"]] = record["Description"]
        
        save_descriptions_to_json(descriptions, "powerdns_descriptions.json")

if __name__ == "__main__":
    main()

