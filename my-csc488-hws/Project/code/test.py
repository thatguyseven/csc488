import pytest
from app import app
import xml.etree.ElementTree as ET

@pytest.fixture
def client():
    """
    Fixture to create a test client for the Flask app.
    """
    app.config['TESTING'] = True  # Configure app for testing
    with app.test_client() as client:
        yield client

def test_load_data(client):
    """
    Call the /load-data endpoint
    Expected Results:
        status_code == 200
        mimetype == "application/xml"
    """
    response = client.post('/load-data')  # Send a POST request with no parameters
    assert response.status_code == 200  # Assert the status code is 200 OK

def test_show_Epochs(client):
    """
    Call the /epoch endpoint
    Expected Results:
        status_code == 200
        mimetype == "application/xml"
        first entry == "2022-042T12:00:00.000Z"
    """
    
    response = client.get('/epoch')  # Send a GET request with no parameters
    assert response.status_code == 200  # Assert the status code is 200 OK
    assert response.content_type in ['application/xml; charset=utf-8', 'text/xml; charset=utf-8'] # Assert response is in XML

    # Match case with raw byte data
    assert b"<epoch>2022-042" in response.data

def test_find_Epoch(client):
    """
    Call the /epoch=<epoch> endpoint
    Expected Results:
        status_code == 200
        mimetype == "application/xml"
        entry (epoch == "2022-042T12:00:00.000Z") exists
    """
    epoch_query = "2022-042T12:00:00.000Z"
    response = client.get(f'/epoch={epoch_query}')  # Send a GET request with one parameter (epoch="2022-042T12:00:00.000Z")
    assert response.status_code == 200  # Assert the status code is 200 OK
    assert response.content_type in ['application/xml; charset=utf-8', 'text/xml; charset=utf-8'] # Assert response is in XML

    # Match cases with raw byte data
    assert b"<epoch>2022-042" in response.data # Match case with epoch in epoch_query
    assert b"-4945.20488742583" in response.data # Match case with x in epoch_query

def test_find_epoch_not_found(client):
    """
    Test case for a request where no data is found for the given epoch.
    Expected Results:
        status_code == 404
    """
    epoch_value = "9999-999"  # An epoch that doesn't exist in the data
    response = client.get(f'/epoch={epoch_value}')  # Send GET request to the endpoint

    # Check that the response status code is 404 (not found)
    assert response.status_code == 404

def test_show_Country(client):
    """
    Call the /countries endpoint
    Expected Results:
        status_code == 200
        mimetype == "application/xml"
        entry (country == "United_States") exists
    """
    response = client.get('/countries')  # Send a GET request with no parameters
    assert response.status_code == 200  # Assert the status code is 200 OK
    assert response.content_type in ['application/xml; charset=utf-8', 'text/xml; charset=utf-8'] # Assert response is in XML

    # Match case
    assert b"<country>United_States" in response.data # Match country entry

def test_find_Country(client):
    """
    Call the /countries=<country> endpoint
    Expected Results:
        status_code == 200
        mimetype == "application/xml"
        entry (country == "United_States") exists
    """
    country_value = "United_States"  # A country that exists in the data
    response = client.get(f'/countries="{country_value}"')  # Send GET request to the endpoint
    assert response.status_code == 200  # Assert the status code is 200 OK
    assert response.content_type in ['application/xml; charset=utf-8', 'text/xml; charset=utf-8'] # Assert response is in XML

    # Match case
    assert b"<country>United_States" in response.data # Assert 'United_States' is returned

def test_country_not_found(client):
    """
    Test case for a request where no data is found for the given country.
    Expected Results:
        status_code == 404
    """
    country_value = "Canada"  # A country that doesn't exist in the data
    response = client.get(f'/countries="{country_value}"')  # Send GET request to the endpoint

    # Check that the response status code is 404 (not found)
    assert response.status_code == 404

def test_show_Region(client):
    """
    Call the /countries=<country>/regions endpoint
    Expected Results:
        status_code == 200
        mimetype == "application/xml"
        Entry (region == "New_Jersey") is returned.
    """
    country_value = "United_States"
    response = client.get(f'/countries="{country_value}"/regions')  # Send a GET request with one parameter (country="United_States")
    assert response.status_code == 200  # Assert the status code is 200 OK
    assert response.content_type in ['application/xml; charset=utf-8', 'text/xml; charset=utf-8'] # Assert response is in XML

    # Match Case
    assert b"<region>New_Jersey" in response.data # Assert region 'New_Jersey' is returned

def test_regions_in_countries_not_in_data(client):
    """
    Test case for a request where no data is found for the given country.
    Expected Results:
        status_code == 404
    """
    country_value = "Canada"  # A country that doesn't exist in the data
    response = client.get(f'/countries="{country_value}"/regions')  # Send GET request to the endpoint

    # Check that the response status code is 404 (not found)
    assert response.status_code == 404

def test_find_Region(client):
    """
    Call the /countries=<country>/regions=<region> endpoint
    Expected Results:
        status_code == 200
        mimetype == "application/xml"
        Entry (region == "New_Jersey") is returned.
    """
    country_value = "United_States"
    region_value = "New_Jersey"
    response = client.get(f'/countries="{country_value}"/regions="{region_value}"')  # Send a GET request with two parameters (country="United_States", region_value="New_Jersey")
    assert response.status_code == 200  # Assert the status code is 200 OK
    assert response.content_type in ['application/xml; charset=utf-8', 'text/xml; charset=utf-8'] # Assert response is in XML

    # Match Cases
    assert b"<region>New_Jersey" in response.data # Assert region 'New_Jersey' is returned
    assert b"<city>Hackensack" in response.data # Assert city 'Hackensack' is returned

def test_regions_not_found(client):
    """
    Test case for a request where no data is found for the given region, country pair.
    Expected Results:
        status_code == 404
    """

    # Test Case 1: Country not found
    country_value = "Canada"  # A country that doesn't exist in the data
    region_value = "New_Jersey"
    response = client.get(f'/countries="{country_value}"/regions="{region_value}"')  # Send a GET request with two parameters (country="United_States", region_value="New_Jersey")

    # Check that the response status code is 404 (not found)
    assert response.status_code == 404

    # Test Case 2: Region not found
    country_value = "United_States"  # A country that doesn't exist in the data
    region_value = "UNKnown"
    response = client.get(f'/countries="{country_value}"/regions="{region_value}"')  # Send a GET request with two parameters (country="United_States", region_value="New_Jersey")

    # Check that the response status code is 404 (not found)
    assert response.status_code == 404

def test_show_Cities(client):
    """
    Call the /countries=<country>/regions=<region>/cities endpoint
    Expected Results:
        status_code == 200
        mimetype == "application/xml"
        Entry (region == "New_Jersey") is returned.
    """
    country_value = "United_States"
    region_value = "New_Jersey"
    response = client.get(f'/countries="{country_value}"/regions="{region_value}"/cities')  # Send a GET request with two parameters (country="United_States", region_value="New_Jersey")
    assert response.status_code == 200  # Assert the status code is 200 OK
    assert response.content_type in ['application/xml; charset=utf-8', 'text/xml; charset=utf-8'] # Assert response is in XML

    # Match Cases
    assert b"<city>Hackensack" in response.data # Assert city 'Hackensack' is returned

def test_cities_in_region_and_countries_not_found(client):
    """
    Test case for a request where no data is found for the given region, country pair.
    Expected Results:
        Test Case 1: status_code == 400
        Test Case 2: status_code == 400
    """

    # Test Case 1: Country not found
    country_value = "Canada"  # A country that doesn't exist in the data
    region_value = "New_Jersey"
    response = client.get(f'/countries="{country_value}"/regions="{region_value}"/cities')  # Send a GET request with incorrect country parameter

    # Check that the response status code is 400 (not found)
    assert response.status_code == 400

    # Test Case 2: Region not found
    country_value = "United_States"  
    region_value = "UNKnown" # A region that doesn't exist in the data
    response = client.get(f'/countries="{country_value}"/regions="{region_value}"/cities')  # Send a GET request with incorrect region parameter 

    # Check that the response status code is 400 (not found)
    assert response.status_code == 400

def test_find_Cities(client):
    """
    Call the /countries=<country>/regions=<region>/cities=<city> endpoint
    Expected Results:
        status_code == 200
        mimetype == "application/xml"
        Entry (region == "New_Jersey") is returned.
    """
    country_value = "United_States"
    region_value = "New_Jersey"
    city_value = "Hackensack"
    response = client.get(f'/countries="{country_value}"/regions="{region_value}"/cities="{city_value}"')  # Send a GET request with three parameters (country="United_States", region_value="New_Jersey", city_value="Hackensack")
    assert response.status_code == 200  # Assert the status code is 200 OK
    assert response.content_type in ['application/xml; charset=utf-8', 'text/xml; charset=utf-8'] # Assert response is in XML

    # Match Cases
    assert b"<city>Hackensack" in response.data # Assert city 'Hackensack' is returned

def test_cities_not_found(client):
    """
    Test case for a request where no data is found for the given region, country pair.
    Expected Results:
        Test Case 1: status_code == 404
        Test Case 2: status_code == 404
        Test Case 3: status_code == 404
    """

    # Test Case 1: Country not found
    country_value = "Canada"  # A country that doesn't exist in the data
    region_value = "New_Jersey"
    city_value = "Hackensack"
    response = client.get(f'/countries="{country_value}"/regions="{region_value}"/cities="{city_value}"')  # Send a GET request with three parameters (country="United_States", region_value="New_Jersey", city_value="Hackensack")

    # Check that the response status code is 400 (not found)
    assert response.status_code == 404

    # Test Case 2: Region not found
    country_value = "United_States"  
    region_value = "UNKnown" # A region that doesn't exist in the data
    response = client.get(f'/countries="{country_value}"/regions="{region_value}"/cities="{city_value}"')  # Send a GET request with three parameters (country="United_States", region_value="New_Jersey", city_value="Hackensack")

    # Check that the response status code is 404 (not found)
    assert response.status_code == 404

    # Check that the response status code is 404 (not found)
    assert response.status_code == 404

    # Test Case 3: City not found
    region_value = "New_Jersey"
    city_value = "UNKnown" # A city that doesn't exist in the data
    response = client.get(f'/countries="{country_value}"/regions="{region_value}"/cities="{city_value}"')  # Send a GET request with three parameters (country="United_States", region_value="New_Jersey", city_value="Hackensack")

    # Check that the response status code is 404 (not found)
    assert response.status_code == 404