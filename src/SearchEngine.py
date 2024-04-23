from bs4 import BeautifulSoup
import requests


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


import random
from urllib.parse import urlparse
from tld import get_tld

import whois
import dns.resolver

class SearchEngine:

    def __init__(self) -> None:
        user_agents = []
        file_path = '/brainboost/brainboost_data/data_tools/tools_goldenthinkerextractor_dataprocessing/resources/user_agents.txt'
        self._domain_extensions = [".com", ".net", ".org", ".io", ".co", ".ai"]
        with open(file_path, 'r') as file:
            for line in file:
                # Remove leading/trailing whitespace and add to the list
                user_agent = line.strip()
                user_agents.append(user_agent)
        self._engines_dict = { 
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
        self._engines = [Google(),Bing(),Yahoo(),Duckduckgo(),Startpage(),Aol(),Dogpile(),Ask(),Mojeek(),Brave(),Torch()]
        pass



    def load_user_agents(self,file_path):
        try:
            with open(file_path, 'r') as f:
                user_agents = [line.strip() for line in f if line.strip()]
            return user_agents
        except Exception as e:
            print(f"Error loading user agents file: {e}")
            return []



    def get_random_user_agent(self):
        user_agents = self.load_user_agents('../resources/user_agents.txt')
        return random.choice(user_agents)



    def source_domainextension_for_country(self,country_name):
        # Dictionary mapping lowercase country names to domain extensions
        country_extensions = {
            "united states": ".com",
            "united kingdom": ".co.uk",
            "germany": ".de",
            "france": ".fr",
            "japan": ".jp",
            "australia": ".au",
            "canada": ".ca",
            "netherlands": ".nl",
            "italy": ".it",
            "spain": ".es",
            "china": ".cn",
            "russia": ".ru",
            "brazil": ".br",
            "mexico": ".mx",
            "switzerland": ".ch",
            "poland": ".pl",
            "sweden": ".se",
            "colombia": ".co",
            "india": ".in",
            "belgium": ".be",
            "austria": ".at",
            "denmark": ".dk",
            "norway": ".no",
            "finland": ".fi",
            "singapore": ".sg",
            "new zealand": ".nz",
            "portugal": ".pt",
            "greece": ".gr",
            "ireland": ".ie",
            "hong kong": ".hk",
            "malaysia": ".my",
            "indonesia": ".id",
            "south africa": ".za",
            "united arab emirates": ".ae",
            "argentina": ".ar",
            "turkey": ".tr",
            "taiwan": ".tw",
            "thailand": ".th",
            "vietnam": ".vn",
            # Add more country-to-extension mappings as needed
        }

        # Convert input country name to lowercase
        country_name_lower = country_name.lower()

        # Lookup the lowercase country name in the dictionary and return the corresponding extension
        return country_extensions.get(country_name_lower, None)

    

    def domain_exists(self, domain):
        domain_assured = domain
        if 'http' in domain:
            domain_assured = self.extract_domain_and_extension(domain)
        try:
            # Check DNS resolution
            answers = dns.resolver.resolve(domain_assured, 'A')
            if answers:
                return True
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            pass
        except dns.exception.DNSException:
            pass

        try:
            # Use WHOIS to get domain registration information
            w = whois.whois(domain_assured)
            if w:
                return True
        except Exception:
            pass

        return False

    def email_available_for_domain(self, domain):
        try:
            # Check DNS resolution for A (IPv4) records
            answers = dns.resolver.resolve(domain, 'A')
            if answers:
                # Check for MX (Mail Exchange) records
                mx_records = dns.resolver.resolve(domain, 'MX')
                if mx_records:
                    return True
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            pass
        except dns.exception.DNSException:
            pass

        # If DNS resolution failed or no MX records found, check WHOIS information
        try:
            w = whois.whois(domain)
            if w:
                return True
        except Exception:
            pass

        return False
    

    
    def extract_domain_and_extension(self,url):
        if 'http' in url:
            try:
                # Parse the URL
                parsed_url = urlparse(url)

                # Get the netloc (domain) from the parsed URL
                domain = parsed_url.netloc

                # Split the domain by '.' to extract the last part as the extension
                domain_parts = domain.split('.')
                extension = domain_parts[-1] if len(domain_parts) > 1 else ''

                # Combine domain and extension with a dot separator
                domain_with_extension = '.'.join([domain, extension])

                return domain_with_extension
            
            except Exception:
                return url
        else:
            return url
        






    def get_company_domain_for_extension(self,company_name=None):

        normalized_company_name = company_name.replace(" ", "").lower()
        for domain_extension in self._domain_extensions:
            possible_domain = normalized_company_name+domain_extension
            if self.domain_exists(possible_domain):
                return possible_domain
        return None
    


    def get_company_domain_for_country(self,company_name,country):
        normalized_company_name = company_name.replace(" ", "").lower()
        possible_domain = normalized_company_name+self.source_domainextension_for_country(country)
        if self.domain_exists(possible_domain):
            return possible_domain
        else:
            return None


         
    def get_company_domain_for(self,company_name,country=None):
        
        def filter_links(links, substring):
            return [s for s in links if self.source_domainextension_for_country(substring) in s]
        
        # Find the best matching root domain containing the company name
        def find_best_matching_domain(company_name, links,country=None):
            company_name_lower = company_name.lower()
            best_match_domain = None
            best_match_length = float('inf')  # Initialize with a large value

            for link in links:
                try:
                    if self.source_domainextension_for_country(country) in link:
                        return link
                    else:
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
        


        if country==None:
            company_domain = self.get_company_domain_for_extension(company_name=company_name)
            if company_domain:
                return company_domain
        else:
            company_domain = self.get_company_domain_for_country(company_name=company_name,country=country)
            if company_domain:
                return company_domain
            else:
                print("No existing domain found, searching using search engines...")
                links = self.search(company_name)
                filtered_links_by_country = filter_links(links, country)
                filtered_links_by_country_that_do_exist = [l for l in filtered_links_by_country if self.domain_exists(l) ]
                filtered_links_that_exist = [l for l in links if self.domain_exists(l) ]
                if len(filtered_links_by_country_that_do_exist) > 1:
                    print("Link for specific country exists: " + str(filtered_links_by_country_that_do_exist))
                    company_domain = find_best_matching_domain(company_name, links=filtered_links_by_country_that_do_exist,country=country)                    
                else:
                    company_domain = find_best_matching_domain(company_name, links=filtered_links_that_exist,country=country)

                print("The company domain is: " + str(company_domain))                    
        return self.extract_domain_and_extension(company_domain)
    




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




    def search(self,q="",engine=None):
        print("Executing Query: " + q)
        
        current_engine = 0
        if engine==None:
            for engine in self._engines:
                try:
                    engine = self._engines[current_engine]
                    results = engine.search(q)
                    links = results.links()
                    if links: 
                        break
                except:
                    current_engine = current_engine + 1
        else:
            results = self._engines_dict[engine].search(q)
            links = results.links()
        return links