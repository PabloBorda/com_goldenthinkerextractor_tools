import json
import SearchEngine

def get_company_domain_for(company_name):
    s = SearchEngine.SearchEngine()
    return s.get_company_domain_for(company_name)

def add_company_domain_to_contacts(json_file_path):
    try:

        # Read contacts from JSON file
        with open(json_file_path, 'r') as file:
            contacts = json.load(file)

        # Process each contact to add company URL
        for contact in contacts:
            company_name = contact['company']
            company_url = get_company_domain_for(company_name)
            contact['domain'] = company_url

        # Write updated contacts back to the JSON file
        with open(json_file_path.split('.')[0]+"with_domains.json", 'w') as file:
            json.dump(contacts, file, indent=4)
        
        print("Company URLs added successfully.")

    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Unable to parse JSON file '{json_file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Provide the absolute path to the JSON file
    json_file_path = '/home/golden/Desktop/Data/com_goldenthinkerextractor_tools/resources/subjective/combined_contacts.json'
    add_company_domain_to_contacts(json_file_path)
