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

class SearchEngine:

    def __init__(self) -> None:
        user_agents = []
        file_path = '/home/golden/Desktop/Data/com_goldenthinkerextractor_tools/resources/user_agents.txt'
        with open(file_path, 'r') as file:
            for line in file:
                # Remove leading/trailing whitespace and add to the list
                user_agent = line.strip()
                user_agents.append(user_agent)
        engines_dict = { 
                    "google":Google(),
                    "bing":Bing(),
                    "yahoo":Yahoo(),
                    "duckduckgo":Duckduckgo(),
                    "startpage":Startpage(),
                    "aol":Aol(),
                    "dogpile":Dogpile(),
                    "ask":Ask(),
                    "mojeek": Mojeek(),
                    "brave": Brave(),
                    "torch": Torch()
        }
        engines = [Google(),Bing(),Yahoo(),Duckduckgo(),Startpage(),Aol(),Dogpile(),Ask(),Mojeek(),Brave(),Torch()]
        pass


    def get_company_domain_for(self,company_name=None):
        def load_user_agents(file_path):
            try:
                with open(file_path, 'r') as f:
                    user_agents = [line.strip() for line in f if line.strip()]
                return user_agents
            except Exception as e:
                print(f"Error loading user agents file: {e}")
                return []

        def get_random_user_agent():
            user_agents = load_user_agents('tools/resources/user_agents.txt')
            return random.choice(user_agents)

        def search(q=""):
            print("Executing Query: " + q)
            engines = [Google(), Bing(), Yahoo(), Duckduckgo(), Startpage(), Aol(), Dogpile(), Ask(), Mojeek(), Brave(), Torch()]
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

        links = search("Company " + company_name)
        if links:
            print("Links returned: " + str(links))
            company_domain = find_matching_domain(company_name, links=links)
            print("The company domain is: " + str(company_domain))
            return company_domain
        else:
            print("Company Domain Not Found")


    def search(self,q="",engine=None):
        print("Executing Query: " + q)
        
        current_engine = 0
        if engine==None:
            for engine in self.engines:
                try:
                    engine = self.engines[current_engine]
                    results = engine.search(q)
                    links = results.links()
                    if links: 
                        break
                except:
                    current_engine = current_engine + 1
        else:
            results = self.engines_dict[engine].search(q)
            links = results.links()
        return links