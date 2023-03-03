import csv
import requests
import json

# Set the Opsgenie API endpoint and API key
api_endpoint = "https://yourAddress.yourDomain"
api_key = "yourAPItoken"

# Set the query parameters for the API request
query_params = {
    "status": "open",
    "priority": "P1,P2,P3,P4,",
    "createdAfter": "2022-10-01T00:00:00Z",
    "createdBefore": "2023-01-31T23:59:59Z",
}

# Set the headers for the API request
headers = {
    "Content-Type": "application/json",
    "Authorization": "GenieKey {}".format(api_key),
}

# Make the API request with the query parameters and headers
response = requests.get(api_endpoint, params=query_params, headers=headers)

# Check the API response status code
if response.status_code != 200:
    print("Failed to get alerts from Opsgenie. Status code: {}".format(response.status_code))
    exit()

# Parse the API response JSON data
response_data = json.loads(response.content)

# Extract the alerts data from the API response
alerts = response_data.get("data", [])

# Check if any alerts were found
if not alerts:
    print("No alerts found.")
    exit()

# Define the CSV output file and header row
output_file = "opsgenie_alerts.csv"
header_row = ["Alert ID", "Message", "Priority", "Created At"]

# Open the output file and write the header row
with open(output_file, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(header_row)

    # Process each alert and write the data to the CSV file
    for alert in alerts:
        alert_id = alert.get("id", "")
        alert_message = alert.get("message", "")
        alert_priority = alert.get("priority", "")
        alert_created_at = alert.get("createdAt", "")

        row = [alert_id, alert_message, alert_priority, alert_created_at]
        writer.writerow(row)

# Print a message indicating the CSV export was successful
print("Data exported to {}".format(output_file))
