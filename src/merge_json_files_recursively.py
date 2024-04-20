import os
import json

def scan_and_combine_contacts(path='.'):
    combined_contacts = []

    def process_json_file(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    combined_contacts.extend(data)
                else:
                    print(f"Ignoring {file_path} as it does not contain an array of contacts.")
        except json.JSONDecodeError:
            print(f"Ignoring {file_path} due to invalid JSON format.")

    def scan_directory(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                scan_directory(item_path)
            elif os.path.isfile(item_path) and item_path.lower().endswith('.json'):
                process_json_file(item_path)

    scan_directory(path)

    # Write out combined contacts to a new JSON file
    output_file_path = os.path.join(path, 'combined_contacts.json')
    with open(output_file_path, 'w') as outfile:
        json.dump(combined_contacts, outfile, indent=4)

    print(f"Combined contacts written to: {output_file_path}")

# Example usage:
if __name__ == "__main__":
    path_to_scan = input("Enter the path to scan (leave empty for current directory): ").strip()
    if not path_to_scan:
        path_to_scan = '.'

    scan_and_combine_contacts(path_to_scan)
