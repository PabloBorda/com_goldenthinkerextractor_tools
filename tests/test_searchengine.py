# Import the centralized setup script
import setup

import pytest
from src.SearchEngine import SearchEngine

@pytest.fixture
def search_instance():
    s = SearchEngine()
    return s

def test_get_company_domain_for(search_instance: SearchEngine):
    # Define the company name for testing
    company_name = "Tesla"
    expected_domain = "tesla.com"
    result_domain = search_instance.get_company_domain_for(company_name)
    assert result_domain == expected_domain

    company_name = "Harvard University"
    expected_domain = "hardvarduniversity.com"
    result_domain = search_instance.get_company_domain_for(company_name)
    assert result_domain == expected_domain
    
    company_name = "BBC"
    expected_domain = "bbc.co.uk"
    result_domain = search_instance.get_company_domain_for(company_name,country="United Kingdom")
    assert result_domain == expected_domain

    company_name = "Greenpeace"
    expected_domain = "greenpeace.org"
    result_domain = search_instance.get_company_domain_for(company_name)
    assert result_domain == expected_domain
    
    company_name = "Louis Vuitton"
    expected_domain = "louisvuitton.eu"
    result_domain = search_instance.get_company_domain_for(company_name)
    assert result_domain == expected_domain
    
    company_name = "Sony"
    expected_domain = "sony.jp"
    result_domain = search_instance.get_company_domain_for(company_name,country="Japan")
    assert result_domain == expected_domain
    
    company_name = "Alibaba"
    expected_domain = "alibaba.cn"
    result_domain = search_instance.get_company_domain_for(company_name,country="China")
    assert result_domain == expected_domain

def test_domain_exists(search_instance: SearchEngine):
    # Test existing domain
    assert search_instance.domain_exists("google.com") == True
    assert search_instance.domain_exists("tesla.io") == True
    assert search_instance.domain_exists("tesla.com") == True
    # Test non-existing domain
    assert search_instance.domain_exists("example.invalid") == False



def test_source_domainextension_for_country(search_instance: SearchEngine):
    # Test known country extensions
    assert search_instance.source_domainextension_for_country("United States") == ".com"
    assert search_instance.source_domainextension_for_country("Germany") == ".de"
    
    # Test unknown country (should return None)
    assert search_instance.source_domainextension_for_country("Unknown Country") == None

