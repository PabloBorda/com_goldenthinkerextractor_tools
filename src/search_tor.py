import requests
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
from stem import SocketError
from search_engines import Google, Bing, Yahoo, Duckduckgo, Startpage, Aol, Dogpile, Ask, Mojeek, Brave, Torch
import random
from urllib.parse import quote_plus

def load_user_agents(file_path):
    try:
        with open(file_path, 'r') as f:
            user_agents = [line.strip() for line in f if line.strip()]
        return user_agents
    except Exception as e:
        print(f"Error loading user agents file: {e}")
        return []

# Define a list of user agent strings for various browsers
user_agents = load_user_agents('tools/resources/user_agents.txt')

# Tor SOCKS proxy configuration
tor_proxy = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

def get_random_user_agent():
    return random.choice(user_agents)

def rotate_tor_ip():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
    except SocketError as e:
        print(f"Error rotating Tor IP: {e}")

def extract_links_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links

def search_with_tor(q=""):
    print("Executing Query: " + q)
    
    headers = {'User-Agent': get_random_user_agent()}

    current_engine = 0
    engines = [Google(), Bing(), Yahoo(), Duckduckgo(), Startpage(), Aol(), Dogpile(), Ask(), Mojeek(), Brave(), Torch()]

    for engine in engines:
        try:
            results = engine.search(q)
            if results and results.links():
                search_url = results.links()[0]
                response = requests.get(search_url, proxies=tor_proxy, headers=headers)
                if response.status_code == 200:
                    return extract_links_from_html(response.content)
        except Exception as e:
            print(f"Error with search engine {type(engine).__name__}: {e}")
            current_engine += 1
            rotate_tor_ip()  # Rotate Tor IP if there's an error

    return None

# Example usage:
search_results = search_with_tor("tesla")
if search_results:
    for link in search_results:
        print(link)
else:
    print("Search failed.")
