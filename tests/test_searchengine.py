
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
        result_domain = search_instance.get_company_domain_for(company_name,country="United States")


        assert result_domain == expected_domain
