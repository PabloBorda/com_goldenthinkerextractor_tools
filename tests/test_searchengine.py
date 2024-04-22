# Import the centralized setup script
import setup

import pytest
from src.SearchEngine import SearchEngine

@pytest.fixture
def search_instance():
    s = SearchEngine()
    return s

def test_get_company_domain_for(search_instance):
    # Define the company name for testing
    company_name = "Tesla"
    
    # Assert that the result is as expected
    expected_domain = "tesla.com"
    
    # Call the function to get the matching domain
    result_domain = search_instance.get_company_domain_for(company_name, country="United States")
    
    assert result_domain == expected_domain

def test_domain_exists(search_instance):
    # Test existing domain
    assert search_instance.domain_exists("google.com") == True
    assert search_instance.domain_exists("tesla.io") == True
    assert search_instance.domain_exists("tesla.com") == True
    # Test non-existing domain
    assert search_instance.domain_exists("example.invalid") == False



def test_source_domainextension_for_country(search_instance):
    # Test known country extensions
    assert search_instance.source_domainextension_for_country("United States") == ".com"
    assert search_instance.source_domainextension_for_country("Germany") == ".de"
    
    # Test unknown country (should return None)
    assert search_instance.source_domainextension_for_country("Unknown Country") == None

