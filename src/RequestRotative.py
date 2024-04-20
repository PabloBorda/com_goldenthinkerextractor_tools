import requests
import json
import random

class RequestRotative:
    def __init__(self, user_agents_file_path='tools/resources/user_agents.txt'):
        self.user_agents_file_path = user_agents_file_path
        self.user_agents = self.load_user_agents()
        self.current_user_agent = None
        self.session = requests.Session()
        self.session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}

    def load_user_agents(self):
        try:
            with open(self.user_agents_file_path, 'r') as f:
                user_agents = [line.strip() for line in f if line.strip()]
            return user_agents
        except Exception as e:
            print(f"Error loading user agents file: {e}")
            return []

    def get_random_user_agent(self):
        if self.user_agents:
            return random.choice(self.user_agents)
        else:
            return None

    def send_request(self, method, url, **kwargs):
        if not self.current_user_agent:
            self.current_user_agent = self.get_random_user_agent()

        headers = kwargs.get('headers', {})
        headers['User-Agent'] = self.current_user_agent
        kwargs['headers'] = headers

        try:
            response = self.session.request(method, url, **kwargs)
            if response.status_code == 200:
                return response
            else:
                print(f"Request failed with status code {response.status_code}")
        except Exception as e:
            print(f"Request failed: {e}")

        return None

    def rotate_user_agent(self):
        self.current_user_agent = self.get_random_user_agent()


# Example usage:
rotator = RequestRotative('resources/user_agents.txt')

# Send a GET request using the rotator (through Tor)
response = rotator.send_request('GET', 'https://google.com')
if response:
    print(response.status_code)
    print(response.text)

# Rotate the user agent
rotator.rotate_user_agent()

# Send another request using the rotated user agent (through Tor)
response = rotator.send_request('GET', 'https://google.com')
if response:
    print(response.status_code)
    print(response.text)
