#!/usr/bin/env python3 
import xmltodict as xml  # Import xmltodict to convert XML into a Python dictionary
from flask import Flask, request, Response, jsonify
import requests
import os
import logging
import json
import pandas as pd

# Global variables for querying
# Use pandas DataFrame for easy querying
position_data = pd.DataFrame()
sighting_data = pd.DataFrame()

# Datapath to local XML file
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Initialize 
logging.basicConfig(level=logging.INFO)


# Non-endpoint Methods
def get_nasa_xml_as_dict(url):
    """
    Retrieves XML files from NASA API.

    Parameters: 
        url (string): A string that contains the API endpoint
	Return: 
        json_content (dict): A dictionary containing the parse  

    Test: 
        RUN = PASS
    """
    print("SENDING HTTP REQUEST...")
    response = requests.get(url)

    print("RESPONSE RECEIVED...")
    xml_content = response.content
    if response.status_code == 200:
        print("PARSING RESPONSE...")
        json_content = xml.parse(xml_content)
        print("EXTRACTING RESULTS...")
        return json_content
    else:
        return {"error": "Failed to retrieve XML file"}

def fetch_positional_data(ephemeris_file="ISS.OEM_J2K_EPH.xml"):
    """
    Retrieves ephemeris position XML file from NASA API. 

	Parameters: 
        ephemeris_file (string): File name for positional data. Default is the NASA API website.
	Return: 
        ephemeris_data (dict): A dictionary containing the sanitized version of the retrieved XML data
    Test:
        RUN - PASS
    """
    filepath = os.path.join(DATA_DIR, ephemeris_file)
    try:
        # Reading from NASA XML file
        logging.info("Fetching ISS.OEM_J2K_EPH.xml...")
        with open(filepath, "r", encoding="utf-8") as file:
            xml_content = file.read()
        logging.info("Fetch Success!")

        # Convert XML to a dictionary
        response = xml.parse(xml_content)

        # Remove extraneous tags
        state_vectors = response["ndm"]["oem"]["body"]["segment"]["data"]["stateVector"]

        # List to store parsed ephemeris data
        ephemeris_data = []  
        
        logging.info("Extracting data...")
        # Loop through each <stateVector> entry and extract data
        for state_vector in state_vectors:
            epoch = state_vector["EPOCH"]  # Extract timestamp
            # Sanitize positional data
            # Extract position coordinates as float
            x = float(state_vector["X"]["#text"]) if isinstance(state_vector["X"], dict) else float(state_vector["X"])
            y = float(state_vector["Y"]["#text"]) if isinstance(state_vector["Y"], dict) else float(state_vector["Y"])
            z = float(state_vector["Z"]["#text"]) if isinstance(state_vector["Z"], dict) else float(state_vector["Z"])

            # Extract velocity components as float
            x_dot = float(state_vector["X_DOT"]["#text"]) if isinstance(state_vector["X_DOT"], dict) else float(state_vector["X_DOT"])
            y_dot = float(state_vector["Y_DOT"]["#text"]) if isinstance(state_vector["Y_DOT"], dict) else float(state_vector["Y_DOT"])
            z_dot = float(state_vector["Z_DOT"]["#text"]) if isinstance(state_vector["Z_DOT"], dict) else float(state_vector["Z_DOT"])

            # Append data as a dictionary to the list
            ephemeris_data.append({
                "epoch": epoch,
                "x": x, "y": y, "z": z,
                "vx": x_dot, "vy": y_dot, "vz": z_dot
            })
            # DEBUG: Prints state_vector 
            # print(state_vector)
        
        logging.info("Extraction successful!")
        return ephemeris_data
    except Exception as e:
        logging.info("Fetch Failed!")
        return {"error": str(e)}

def fetch_sighting_data(sighting_file = "XMLsightingData_citiesUSA07.xml"):
    """
    Retrieves XMLsightingData_citiesUSA07.xml file from NASA API and sanitizes the positional data as floats for analysis.

	Parameters: 
        sighting_file (string): File name for ISS Sighting Data XML file. Default is 'XMLsightingData_citiesUSA07.xml'.
        sighting_url = "https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA07.xml"
	Return: 
        visible_pass_data (dict): A dictionary containing all visible pass data 
    Test:
        RUN - PASS
    """
    filepath = os.path.join(DATA_DIR, sighting_file)
    try:
        # Reading from NASA XML file
        logging.info("Fetching XMLsightingData_citiesUSA07.xml...")
        with open(filepath, "r", encoding="utf-8") as file:
            xml_content = file.read()
        logging.info("Fetch Success!")

        # Convert XML to a dictionary
        response = xml.parse(xml_content)

        # Extract the list of visible passes
        visible_passes = response['visible_passes']['visible_pass']
        
        # Create storage for sighting data
        visible_pass_data = []
        
        logging.info("Extracting data...")
        # Loop through each visible pass and extract its data
        for pass_data in visible_passes:
            country = pass_data['country']
            region = pass_data['region']
            city = pass_data['city']
            spacecraft = pass_data['spacecraft']
            sighting_date = pass_data['sighting_date']
            duration_minutes = pass_data['duration_minutes']
            max_elevation = pass_data['max_elevation']
            enters = pass_data['enters']
            exits = pass_data['exits']
            utc_offset = pass_data['utc_offset']
            utc_time = pass_data['utc_time']
            utc_date = pass_data['utc_date']
            
            visible_pass_data.append({
                "country": country, "region": region, "city": city, 
                "spacecraft": spacecraft,
                "sighting_date": sighting_date, "vy": duration_minutes, "vz": max_elevation,
                "enters": enters, "exits": exits,
                "utc_offset": utc_offset, "utc_time": utc_time, "utc_date": utc_date
            })
            # DEBUG: Prints state_vector 
            # print(pass_data)
        logging.info("Extraction successful!")
        return visible_pass_data
    except Exception as e:
        logging.info("Fetch Failed!")
        return {"error": str(e)}

def save_to_xml(data, filename="data.xml"):
    """
    Saves data into /data directory in the Project directory. File is saves as a .xml file for querying.

	Parameters: 
        data (DataFrame): Data to be stored in XML format
        filename (string): string of the filepath to /data directory
	Return: 
        None
    Test:
        RUN - FAIL
    """
    # Define the full file path in the DATA_DIR
    filepath = os.path.join(DATA_DIR, filename)
    
    # Set root and row elements
    root_element = "entries"
    row_element = "entry"

    logging.info(f"Saving data to {filename} in {filepath}")
    
    # STEP 1: Check if the file exists in the correct directory
    if os.path.exists(filepath):
        # If file exists, parse its content using xmltodict
        try:
            # Opens the file and parses the contents
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
                xml_data = xml.parse(content)  # Convert XML to dictionary
            
            # If the XML structure is not what we expect, reinitialize it
            if "entries" not in xml_data:
                raise ValueError("Unexpected XML structure.")
        
        except Exception as e:
            logging.error(f"Error reading the existing XML file: {e}")
            
            # Initialize an empty structure if the file is invalid
            xml_data = {root_element: {row_element: []}}
    else:
        # If the file does not exist, initialize a new root structure
        xml_data = {root_element: {row_element: []}}

    # STEP 2: Convert data to dict format
    dict_data = df_to_dict(data, root_element, row_element)
    rows = dict_data[root_element][row_element]
    
    # STEP 3: Append new dict_data to the dictionary (Ensure data is in correct format)
    for row in rows:
        # Each row must be a dictionary with key-value pairs
        if isinstance(row, dict):
            xml_data[root_element][row_element].append(row)
        else:
            logging.warning("Skipped a row that was not a dictionary.")

    # STEP 4: Write the updated dictionary back to XML using xmltodict.unparse
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(xml.unparse(xml_data, pretty=True))  # Convert dict back to XML
        logging.info(f"SUCCESS: Data saved to {filename} in {filepath}")
    except Exception as e:
        logging.error(f"Error writing XML file: {e}")

def load_from_xml(filename="data.xml"):
    """
    Reads data from a file /data directory in the Project directory. File is saves as a .xml file for querying.

	Parameters: 
        filename (string): string of the filepath to /data directory
	Return: 
        content (dict): The contents of the .xml file
    """
    filepath = os.path.join(DATA_DIR, filename)
    
    try:
        logging.info(f"Loading data from {filename} in {filepath}")
        # Read the XML file
        with open(filepath, "r", encoding="utf-8") as file:
            xml_content = file.read()
        
        # Convert XML to a dictionary
        xml_data = xml.parse(xml_content)

        # Removing extra data
        content = xml_data["entries"]["entry"]

        logging.info(f"SUCCESS: Data extracted from {filename} in {filepath}")
        # Return contents of XML file as a dict
        return content

    except Exception as e:
        logging.info(f"ERROR: Could not find file {filename} in {DATA_DIR}")
        return({"error": str(e)})

def dict_to_df(data_dict):
    """
    Converts a dictionary to a pandas DataFrame.

    Parameters:
        data_dict (dict): A dictionary where keys are column names and values are lists of column data.

    Return: 
        Pandas DataFrame with contents of data_dict
    """
    try:
        # Convert dict to DataFrame
        df = pd.DataFrame(data_dict)
        return df
    except Exception as e:
        # If conversion fails, return empty dataframe
        print(f"Error converting dict to DataFrame: {e}")
        return pd.DataFrame()

def df_to_dict(df, root_element = "entries", row_element = "entry", orient='records'):
    """
    Converts a pandas DataFrame to a dictionary.

    Parameters:
        df (DataFrame): The pandas DataFrame to convert.
        orient (string): Orientation of the dict (e.g., 'records', 'dict', 'list', etc.)
    Return:
        Python dictionary based on the chosen orientation.
    """
    try:
        df.columns = df.columns.astype(str)
        data_dict = {
            root_element: {
                row_element: df.to_dict(orient="records")
            }
        }
        # Convert from dataframe to dict
        return data_dict
    
    except Exception as e:
        # Conversion not possible
        print(f"Error converting DataFrame to dict: {e}")
        return {}

# Endpoints
app = Flask(__name__)

@app.route("/", methods=['GET'])
def greet() -> Response:
    """
    Prints greeting message when accessing base address. 

    Parameters: 
        None

    Return:
        flask.Response object containing instructions in plaintext
    """
    logging.info("Instructions queried")
    # STEP 1: Prepare instruction message
    instructions = {
        "ISS Tracking API\n\n"
        "Endpoints:\n"
        
        "Load Data -> POST /load-data | Retrieves data from NASA API and saves it to the server. \n\n"

        "Epoch Data -> GET /epoch | Retrieves all epochs in positional data\n\n"
        "Specific Epoch Data -> GET /epoch=<epoch> | Retrieves specific epoch with specific flight time. Epoch must be a string.\n\n"
        "Country Data -> GET /countries | Retrieves all countries in sighting data.\n\n"
        "Specific Country Data -> GET /countries=<country> | Retrieves all entries in a specific country in sighting data. Country must be a string.\n\n"
        "Region Data -> GET /countries=<country>/regions | Retrieves all regions within a country in sighting data. Country must be a string.\n\n"
        "Specific Region Data -> GET /countries=<country>/regions=<region> | Retrieves all entries in a specific region witin a country in sighting data. Country and region must be a string.\n\n"
        "City Data -> GET /countries=<country>/regions/cities | Retrieves all cities in sighting data specified country and region. Country and region must be strings.\n\n"
        "Specific City Data -> GET /countries=<country>/regions=<region>/cities=<city> | Retrieves all entries about a specific city in a specified country and region sighting data. Country, region, and city must be a string.\n\n"
    }

    # STEP 2: Return instruction message
    return Response(instructions, mimetype='text/plain')

@app.route("/load-data", methods=['POST'])
def load_data() -> Response:
    """
    Loads https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml as positional data
    and https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA07.xml as sighting data
    into program memory.

    Parameters: 
        None
    
    Returns:
        flask.Response object containing success message.

    Tests:
        Run: PASS
    """
    logging.info("POST /load-data request received.")

    global position_data, sighting_data
    try: 
        # STEP 1: Check if requested files are present on device. Use the default values if no request is made.
        positional_file = request.files.get("positional_file")
        sighting_file = request.files.get("sighting_file")
        
        # ERROR HANDLING: Sets file names if file names were not specified in POST request

        if not positional_file:
            # Uses POSITIONAL_DATA.xml if no data has been loaded
            positional_file = "POSITIONAL_DATA.xml"
        else: 
            positional_file.save(os.path.join(DATA_DIR, f"{positional_file}"))

        if not sighting_file: 
            # Uses SIGHTING_DATA.xml if no data has been loaded
            sighting_file = "SIGHTING_DATA.xml"
        else: 
            sighting_file.save(os.path.join(DATA_DIR, f"{sighting_file}"))

        logging.info("BEGIN: FETCHING ISS FLIGHT DATA & ISS SIGHTING DATA IN US...")

        # Check if existing file has already been extracted from NASA API
        if (not os.path.isfile(os.path.join(DATA_DIR, positional_file))) and (position_data.shape[0] == 0):

            # If the data file does not exist and the data has not been loaded, fetch data from NASA API
            logging.info("BEGIN: FETCHING ISS FLIGHT DATA...")

            # Saves result as a pandas DataFrame
            position_data = dict_to_df(fetch_positional_data())

            logging.info("BEGIN: SAVING TO DIRECTORY")
            
            # Save data to local XML file
            save_to_xml(position_data, positional_file)
            logging.info("END: SAVED")
        else: 
            # Otherwise, fetch data from the local XML file
            position_data = dict_to_df(load_from_xml(positional_file))

        # Check if existing file has already been extracted from NASA API
        if (not os.path.isfile(os.path.join(DATA_DIR, sighting_file))) and (sighting_data.shape[0] == 0):

            # If the data file does not exist and the data has not been loaded, fetch data from NASA API
            logging.info("BEGIN: FETCHING ISS SIGHTING DATA...")
            sighting_data = dict_to_df(fetch_sighting_data())

            logging.info("BEGIN: SAVING TO DIRECTORY")
            
            # Save data to local XML file
            save_to_xml(sighting_data, sighting_file)
            logging.info("END: SAVED")
        else: 
            # Otherwise, fetch data from the local XML file
            sighting_data = dict_to_df(load_from_xml(sighting_file))

        logging.info("END: FETCHING COMPLETE")

        """
        # DEBUG: Print result of fetch methods
        for row in positional_data:
            print(row)
        for row in sighting_data:
            print(row)
        """

        # STEP 2: Return Retrieval results

        logging.info("SUCCESS: Data has been loaded.")
        # Return Success message
        return jsonify({'message': 'Data downloaded and saved successfully.'})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Could not find: {str(e)}'}), 400

@app.route("/epoch", methods=['GET'])
def show_Epochs() -> Response:
    """
    Queries pandas DataFrame for all EPOCH strings and returns all epochs as an XML Response.

    Args:
        None
    
    Returns:
        epoch_xml (XML): XML Response containing all Epochs in positional data.
    """
    logging.info("GET /epoch request.")
    try:
        logging.info("Retrieving EPOCH data...")

        # STEP 1: Query POSITIONAL_DATA for epoch list
        result = position_data["epoch"].to_frame()
        epoch_xml = result.to_xml(root_name='epochs', row_name='EPOCH', index=False, parser="etree")
        
        # STEP 2: Prepare return message with XML attachment and return result

        logging.info("SUCCESS: Epoch retrieval successful!")
        # Return the XML with the appropriate Content-Type header
        return Response(epoch_xml, mimetype='application/xml')
    except Exception as e:
        logging.info("ERROR: Epoch retrieval failed!")
        
        # Prepare error message
        error_message = {"error": str(e), "message": "An error has occurred."}

        # Return the error message with the appropriate Content-Type header
        return_message = Response(response=json.dumps(error_message), status=400, mimetype="application/json")
        return return_message

@app.route("/epoch=<epoch>", methods=['GET'])
def find_Epoch(epoch) -> Response:
    """
    Uses epoch data to return all data about an Epoch. Queries a pandas DataFrame for a specific EPOCH. Returns Epoch data as an XML Response.

	Parameters: 
        epoch (string): String containing EPOCH data field from positional_data
	Return: 
        epoch_data (XML): All data in positional data with a matching epoch.
    """
    logging.info("GET /epoch=<epoch> request.")
    try:
        logging.info(f"Retrieving {epoch} data...")

        # STEP 1: Query POSITIONAL_DATA for specific epoch list
        result = position_data[position_data["epoch"].str.startswith(f"{epoch}")].drop_duplicates()

        # ERROR HANDLING: Empty Query Result
        if result.empty:
            logging.info("ERROR: Epoch not in positional data")
            # Returns an error if no results are found
            return Response({"error": "Epoch not Found", "message": "Queried epoch is not in sighting data."}, status=404, mimetype="application/xml")
        
        # epoch_data = result.to_frame()
        epoch_xml = result.to_xml(root_name='epochs', row_name='EPOCH', index=False, parser="etree")
        
        # STEP 2: Prepare return message with XML attachment and return result
        logging.info("SUCCESS: Epoch data retrieval successful!")
        # Return the XML with the appropriate Content-Type header
        return Response(epoch_xml, mimetype="application/xml")
    
    except Exception as e:
        logging.info("ERROR: Epoch data retrieval failed!")
        
        # Prepare error message
        error_message = {"error": str(e), "message": "An error has occurred."}

        # Return the error message with the appropriate Content-Type header
        return_message = Response(response=json.dumps(error_message), status=400, mimetype="application/json")
        return return_message

@app.route("/countries", methods=['GET'])
def show_Country() -> Response:
    """
    Queries sighting data for all countries in the file. Returns country names as an XML Response.

	Parameters: 
        none
	Return: 
        country_data (XML): XML Response containing all country names in sighting data.
    """
    logging.info("GET /countries request.")
    try:
        logging.info("Retrieving COUNTRY data...")

        # STEP 1: Query SIGHTING_DATA for country list
        result = sighting_data["country"].to_frame().drop_duplicates()
        
        # STEP 2: Prepare return message with XML attachment and return result
        logging.info("SUCCESS: Country data retrieval successful!")
        country_xml = result.to_xml(root_name='countries', row_name='COUNTRY', index=False, parser="etree")

        # Return the XML with the appropriate Content-Type header
        return Response(country_xml, mimetype='application/xml')
    
    except Exception as e:
        logging.info("ERROR: Country data retrieval failed!")
        
        # Prepare error message
        error_message = {"error": str(e), "message": "An error has occurred."}

        # Return the error message with the appropriate Content-Type header
        return_message = Response(response=json.dumps(error_message), status=400, mimetype="application/json")
        return return_message

@app.route("/countries=<country>", methods=['GET'])
def find_Country(country) -> Response:
    """
    Queries sighting data for specific country. Returns country data as a XML Response.

	Parameters: 
        country (string): Queried country name
	Return: 
        country_data (XML): XML Response containing all country names in sighting data.
    """

    logging.info("GET /countries=<country> request.")
    try:
        print(sighting_data.head())
        
        logging.info(f"Retrieving COUNTRY={country} data...")

        # STEP 1: Query SIGHTING_DATA for specific country
        result = sighting_data.query(f'country=={country}').drop_duplicates()
        
        # ERROR HANDLING: Empty Query Result
        if result.empty:
            logging.info("ERROR: Country not in sighting data")
            # Returns an error if no results are found
            return Response({"error": "Country not Found", "message": "Queried country is not in sighting data."}, status=404, mimetype="application/xml")
        
        # STEP 2: Prepare return message with XML attachment and return result
        logging.info("SUCCESS: Country data retrieval successful!")
        country_data = result.to_xml(root_name='epochs', row_name='EPOCH', index=False, parser="etree")
        # Return the XML with the appropriate Content-Type header
        return Response(country_data, mimetype='application/xml')
    
    except Exception as e:
        logging.info("ERROR: Country data retrieval failed!")
        
        # Prepare error message
        error_message = {"error": e, "message": "An error has occurred."}

        # Return the error message with the appropriate Content-Type header
        return_message = Response(response=json.dumps(error_message), status=400, mimetype="application/json")
        return return_message

@app.route("/countries=<country>/regions", methods=['GET'])
def show_Region(country) -> Response:
    """
    Queries sighting data for regions in a specific country. Returns region names as a XML Response.

	Parameters: 
        country (string): Queried country name
	Return: 
        region_data (XML): XML Response containing all regions located in queried country in sighting data.
    """

    logging.info("GET /countries=<country>/regions request.")
    try:
        logging.info(f"Retrieving regions in {country} data...")

        # STEP 1: Query SIGHTING_DATA for regions in specific country
        result = sighting_data.query(f'country=={country}').drop_duplicates()
        result = result["region"].to_frame().drop_duplicates()

        # ERROR HANDLING: Empty Query Result
        if result.empty:
            logging.info("ERROR: Country not in sighting data")
            # Returns an error if no results are found
            return Response(
                response=json.dumps({"error": "Country not Found", "message": "Queried country is not in sighting data."}), 
                status=404, 
                mimetype="application/xml")
        
        region_data = result.to_xml(root_name='regions', row_name='REGION', index=False, parser="etree")
        
        # STEP 2: Prepare return message with XML attachment and return result
        logging.info("SUCCESS: Region data retrieval successful!")
        # Return the XML with the appropriate Content-Type header
        return Response(region_data, mimetype='application/xml')
    
    except Exception as e:
        logging.info("ERROR: Region data retrieval failed!")
        
        # Prepare error message
        error_message = {"error": str(e), "message": "An error has occurred."}

        # Return the error message with the appropriate Content-Type header
        return_message = Response(response=json.dumps(error_message), status=400, mimetype="application/json")
        return return_message

@app.route("/countries=<country>/regions=<region>", methods=['GET'])
def find_Region(country, region) -> Response:
    """
    Queries sighting data for specific region in a specific country. Returns region data as a XML Response.

	Parameters: 
        country (string): Queried country name
        region (string): Queried region name
	Return: 
        region_data (XML): XML Response containing all regions located in queried country in sighting data.
    """

    logging.info("GET /countries=<country>/regions=<region> request.")
    try:
        logging.info(f"Retrieving region={region} in {country} data...")

        # STEP 1: Query SIGHTING_DATA for specific region in specified country
        result = sighting_data.query(f'country=={country} and region=={region}').drop_duplicates()
    
        # ERROR HANDLING: Empty Query Result
        if result.empty:
            logging.info("ERROR: Region not in sighting data")
            # Returns an error if no results are found
            return Response(
                response=json.dumps({"error": "Region not Found", "message": "Queried region is not in sighting data."}), 
                status=404, 
                mimetype="application/xml")
        
        region_data = result.to_xml(root_name='regions', row_name='REGION', index=False, parser="etree")
        
        # STEP 2: Prepare return message with XML attachment and return result
        logging.info("SUCCESS: Region data retrieval successful!")
        # Return the XML with the appropriate Content-Type header
        return Response(region_data, mimetype='application/xml')
    
    except Exception as e:
        logging.info("ERROR: Region data retrieval failed!")
        
        # Prepare error message
        error_message = {"error": str(e), "message": "An error has occurred."}

        # Return the error message with the appropriate Content-Type header
        return_message = Response(response=json.dumps(error_message), status=400, mimetype="application/json")
        return return_message

@app.route("/countries=<country>/regions=<region>/cities", methods=['GET'])
def show_City(country, region) -> Response:
    """
    Queries sighting data for cities in region in a specified country. Returns city name data as a XML Response.

	Parameters: 
        country (string): Queried country name
        region (string): Queried region name
	Return: 
        city_data (XML): XML Response containing all regions located in queried country in sighting data.
    """

    logging.info("GET /countries=<country>/regions=<region>/cities request.")
    try:
        logging.info(f"Retrieving cities in {region}, {country} data...")

        # STEP 1: Query SIGHTING_DATA for cities in specific region in specified country
        result = sighting_data.query(f'country=={country} and region=={region}').drop_duplicates()
        result = result["city"].to_frame().drop_duplicates()

        # ERROR HANDLING: Empty Query Result
        if result.empty:
            logging.info("ERROR: Region not in sighting data")
            # Returns an error if no results are found
            return Response(
                message=json.dumps({"error": "Region not Found", "message": "Queried region is not in sighting data."}), 
                status=404, 
                mimetype="application/xml")
        
        city_data = result.to_xml(root_name='cities', row_name='CITY', index=False, parser="etree")
        
        # STEP 2: Prepare return message with XML attachment and return result
        logging.info("SUCCESS: City data retrieval successful!")
        # Return the XML with the appropriate Content-Type header
        return Response(city_data, mimetype='application/xml')
    
    except Exception as e:
        logging.info("ERROR: City data retrieval failed!")
        
        # Prepare error message
        error_message = {"error": str(e), "message": "An error has occurred."}

        # Return the error message with the appropriate Content-Type header
        return_message = Response(response=json.dumps(error_message), status=400, mimetype="application/json")
        return return_message

@app.route("/countries=<country>/regions=<region>/cities=<city>", methods=['GET'])
def find_City(country, region, city) -> Response:
    """
    Queries sighting data for cities in region in a specified country. Returns city name data as a XML Response.

	Parameters: 
        country (string): Queried country name
        region (string): Queried region name
        city (string): Queried city name
	Return: 
        city_data (XML): XML Response containing all regions located in queried country in sighting data.
    """

    logging.info("GET /countries=<country>/regions=<region>/cities=<city> request.")
    try:
        logging.info(f"Retrieving {city} in {region}, {country} data...")

        # STEP 1: Query SIGHTING_DATA for city in specific region in specified country
        result = sighting_data.query(f'country=={country} and region=={region} and city=={city}').drop_duplicates()
        
        # ERROR HANDLING: Empty Query Result
        if result.empty:
            logging.info("ERROR: City not in sighting data")
            # Returns an error if no results are found
            return Response(
                response=json.dumps({"error": "City not Found", "message": "Query is not in sighting data."}), 
                status=404, 
                mimetype="application/xml")
        
        city_data = result.to_xml(root_name='cities', row_name='CITY', index=False, parser="etree")
        
        # STEP 2: Prepare return message with XML attachment and return result
        logging.info("SUCCESS: City data retrieval successful!")
        # Return the XML with the appropriate Content-Type header
        return Response(city_data, mimetype='application/xml')
    
    except Exception as e:
        logging.info("ERROR: City data retrieval failed!")
        
        # Prepare error message
        error_message = {"error": str(e), "message": "An error has occurred."}

        # Return the error message with the appropriate Content-Type header
        return_message = Response(response=json.dumps(error_message), status=400, mimetype="application/json")
        return return_message

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)