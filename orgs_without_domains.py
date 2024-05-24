"""
File: orgs_without_domains.py
Author: Sushant Awalekar
Date: May 24 2024
Email : sushantawalekar@gmail.com

Description:
This script retrieves organizations from a zendesk and filters out those without associated domain names.

Usage:
1. Ensure you have the necessary permissions to access the Zendesk Orgs.
2. Replace <username> <password> <subdomain> with actual zendesk details.
2. Run the script using a Python environment or Jupyter Notebook.

Requirements:
- Python 3.x

"""

import requests
import csv

username = "<username>"
password = "<password>"

url = "https://<subdomain>.zendesk.com/api/v2/organizations"
headers = {
	"Content-Type": "application/json",
}

def get_organizations(url, username, password, headers):
    """
    Retrieves organizations from the zendesk with pagination support.
    Args:
        url (str): The base URL of the API endpoint.
        username (str): The username for authentication.
        password (str): The password for authentication.
        headers (dict): Additional headers for the request.
    Returns:
        List of organization data.
    """
    organizations = []
    page = 1
    while True:
        # Make a request for the current page
        params = {"page": page}
        response = requests.get(url, auth=(username, password), headers=headers, params=params)
        data = response.json()

        # Check if there are organizations in the response
        current_orgs = data.get("organizations", [])
        if not current_orgs:
            break

        # Add organizations from the current page to the list
        organizations.extend(current_orgs)

        # Check if there are more pages
        if not data.get("next_page"):
            break

        # Move to the next page
        page += 1

    return organizations

organizations = get_organizations(url, username, password, headers)

empty_domains = []

for org in organizations:
  if not org['domain_names']:
    empty_domains.append(org['name'])

# Export to CSV
csv_filename = 'empty_domains.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Name'])
    for name in empty_domains:
        csvwriter.writerow([name])

print(f"Names of organizations with empty domain_names have been exported to {csv_filename}.")
