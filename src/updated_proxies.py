import requests
import json
import schedule
import time

def download_json_file(url, output_file):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_file, 'w') as f:
                json.dump(response.json(), f)
            print(f"Downloaded JSON file from {url} to {output_file}")
        else:
            print(f"Failed to download JSON file from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred during download: {e}")

def job():
    url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.json"
    output_file = "resources/proxies.json"
    download_json_file(url, output_file)

# Schedule the job to run every 10 minutes
schedule.every(10).minutes.do(job)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
