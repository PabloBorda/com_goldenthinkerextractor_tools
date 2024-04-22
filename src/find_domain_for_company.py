import requests
import random
from urllib.parse import urlparse
from search_engines import Aol, Ask, Bing, Dogpile, Duckduckgo, Google, Mojeek, Startpage, Torch, Brave, Yahoo
from tld import get_tld

# Load user agents from a file
def load_user_agents(file_path):
    try:
        with open(file_path, 'r') as f:
            user_agents = [line.strip() for line in f if line.strip()]
        return user_agents
    except Exception as e:
        print(f"Error loading user agents file: {e}")
        return []

# Generate a random user agent
def get_random_user_agent():
    return random.choice(load_user_agents('/home/golden/Desktop/brainboost_data/data_tools/tools_goldenthinkerextractor/../resources/user_agents.txt'))

# Check if a domain exists by sending an HTTP HEAD request
def domain_exists(domain):
    try:
        response = requests.head(f"http://{domain}")  # Check if domain is accessible
        return response.status_code == 200  # Check if HTTP status code is 200 (OK)
    except requests.exceptions.RequestException:
        return False  # Any exception or non-200 response indicates domain does not exist

# Generate possible domain names based on company name and domain extensions
def generate_possible_domains(company_name, domain_extensions):
    company_name = company_name.lower().replace(" ", "")
    possible_domains = [company_name + ext for ext in domain_extensions]
    return possible_domains

# Get an existing domain by checking multiple domain extensions
def get_existing_domain(company_name, domain_extensions):
    possible_domains = generate_possible_domains(company_name, domain_extensions)
    for domain in possible_domains:
        if domain_exists(domain):
            return domain
    return None  # If no existing domain found

# Search function using search engines
def search(q=""):
    print("Executing Query: " + q)
    engines = [Google(), Bing(), Yahoo(), Duckduckgo(), Startpage(), Aol(), Dogpile(), Ask(), Mojeek(), Brave(), Torch()]
    for engine in engines:
        try:
            results = engine.search(q)
            links = results.links()
            if links:
                return links
        except:
            pass
    return []  # Return empty list if no links are found

# Find the best matching link containing the company name
def find_matching_link(company_name, links):
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

# Find the best matching root domain containing the company name
def find_matching_domain(company_name, links):
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

# Get company website link using domain testing and search engines
def get_company_website_link_for(company_name=None):
    domain_extensions = [
        ".com", ".net", ".org", ".io", ".co", ".ai", ".app", ".tech", ".design", ".online", ".blog"
        # Add more domain extensions here as needed
    ]

    # Check if there's an existing domain based on company name and extensions
    existing_domain = get_existing_domain(company_name, domain_extensions)

    if existing_domain:
        print(f"Existing domain found: http://{existing_domain}")
        return f"http://{existing_domain}"
    else:
        print("No existing domain found, searching using search engines...")
        links = search("Company " + company_name)
        if links:
            print("Links returned: " + str(links))
            company_url = find_matching_link(company_name, links=links)
            print("The company URL is: " + str(company_url))
            return company_url
        else:
            print("Company website not found")

# Get company domain using domain testing and search engines
def get_company_domain_for(company_name=None):
    domain_extensions = [
        ".com", ".net", ".org", ".io", ".co", ".ai", ".app", ".tech", ".design", ".online", ".blog"
        # Add more domain extensions here as needed
    ]

    # Check if there's an existing domain based on company name and extensions
    existing_domain = get_existing_domain(company_name, domain_extensions)

    if existing_domain:
        print(f"Existing domain found: {existing_domain}")
        return existing_domain
    else:
        print("No existing domain found, searching using search engines...")
        links = search("Company " + company_name)
        if links:
            print("Links returned: " + str(links))
            company_domain = find_matching_domain(company_name, links=links)
            print("The company domain is: " + str(company_domain))
            return company_domain
        else:
            print("Company domain not found")

# Example usage:
# company_name = "Example Company"
# get_company_website_link_for(company_name)
# get_company_domain_for(company_name)
