import json

def get_domain_from_company(company_name):
    # Simulate retrieving domain from company name (using a cache)
    domain_cache = {
        "blobrock": "blobrock.com",
        "Angel Investor Forum": "angelinvestorforum.com"
        # Add more mappings as needed
    }
    return domain_cache.get(company_name, None)

def process_objects_with_domains(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    modified_objects = []
    seen_companies = set()

    for obj in data:
        company_name = obj.get('company')
        if company_name not in seen_companies:
            # Get domain for the company (retrieve from cache if available)
            domain = get_domain_from_company(company_name)
            seen_companies.add(company_name)

        # Create a new object with the added 'domain' field
        modified_obj = {**obj, 'domain': domain}
        modified_objects.append(modified_obj)

    # Generate output filename based on input filename
    output_filename = input_file.replace('.json', f'_domain_added.json')

    # Write modified objects to a new JSON file
    with open(output_filename, 'w') as f:
        json.dump(modified_objects, f, indent=4)

    print(f"Modified objects written to: {output_filename}")

# Example usage
if __name__ == "__main__":
    input_file = 'resources/resources_data/data_subjective/combined_contacts.json'  # Specify the input JSON file containing the array of objects
    process_objects_with_domains(input_file)
