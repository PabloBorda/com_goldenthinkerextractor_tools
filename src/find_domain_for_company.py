from search_engines import Google
from search_engines import Bing
from search_engines import Yahoo
from search_engines import Duckduckgo
from search_engines import Startpage
from search_engines import Aol
from search_engines import Dogpile
from search_engines import Ask
from search_engines import Mojeek
from search_engines import Brave
from search_engines import Torch


import requests
import random
from urllib.parse import urlparse
from tld import get_tld

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


def get_random_user_agent():
    return random.choice(user_agents)

def get_webpage_text(url):
    try:
        random_user_agent = get_random_user_agent()
        response = requests.get(url, headers={"User-Agent": random_user_agent})
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def search(q=""):
    print("Executing Query: " + q)
    engines = [Google(),Bing(),Yahoo(),Duckduckgo(),Startpage(),Aol(),Dogpile(),Ask(),Mojeek(),Brave(),Torch()]
    current_engine = 0
    for engine in engines:
        try:
            engine = engines[current_engine]
            results = engine.search(q)
            links = results.links()
            if links: 
               break
        except:
            current_engine = current_engine + 1
        
    return links



def find_matching_link(company_name, links):
    """
    This function finds the link in the list that best matches the company name,
    considering company name presence in base domain and base domain length.

    Args:
        company_name (str): The company name to match against.
        links (list): A list of URLs.

    Returns:
        str: The URL with the shortest base domain containing the company name, or None if no match is found.
    """

    company_name_lower = company_name.lower()
    best_match = None
    best_match_length = float('inf')  # Initialize with a large value

    for link in links:
        try:
            parsed_url = urlparse(link)
            domain = get_tld(link, as_object=True).domain.lower()  # Get base domain

            if company_name_lower in domain:
                domain_length = len(domain)
                if domain_length < best_match_length:
                    best_match = link
                    best_match_length = domain_length

        except (ValueError, AttributeError):  # Handle invalid URLs or domain extraction errors gracefully
            pass

    return best_match



def find_matching_domain(company_name, links):
    """
    This function finds the root domain (without subdomains) in the list that best matches the company name,
    considering company name presence in the root domain and domain length.

    Args:
        company_name (str): The company name to match against.
        links (list): A list of URLs.

    Returns:
        str: The root domain (without subdomains) with the shortest length containing the company name,
             or None if no match is found.
    """

    company_name_lower = company_name.lower()
    best_match_domain = None
    best_match_length = float('inf')  # Initialize with a large value

    for link in links:
        try:
            parsed_url = urlparse(link)
            netloc_parts = parsed_url.netloc.split('.')  # Split netloc into parts
            root_domain = '.'.join(netloc_parts[-2:])  # Get last two parts for root domain

            if company_name_lower in root_domain:
                domain_length = len(root_domain)
                if domain_length < best_match_length:
                    best_match_domain = root_domain
                    best_match_length = domain_length

        except (ValueError, AttributeError):  # Handle invalid URLs or domain extraction errors gracefully
            pass

    return best_match_domain



def get_company_website_link_for(company_name=None):
    links = search("Company " + company_name)
    if links:
        print("Links returned: " + str(links))
        company_url = find_matching_link(company_name,links=links)
        print("The company url is: " + str(company_url))
        return company_url
    else:
        print("Company Website Not Found")
   

def get_company_domain_for(company_name=None):
    links = search("Company " + company_name)
    if links:
        print("Links returned: " + str(links))
        company_domain = find_matching_domain(company_name,links=links)
        print("The company domain is: " + str(company_domain))
        return company_domain
    else:
        print("Company Domain Not Found")


