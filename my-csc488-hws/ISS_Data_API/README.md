# ISS Data API
The ISS Data API is a Flask-based web API designed to query the following datasets:

| File Name | Dataset | 
| - | - | 
| ISS.OEM_J2K_EPH.xml | Contains data pertaining to ISS flight paths. Contains coordinates (in kilometers) and distance vectors (in kilometers/second) in 3 dimensions (represented as x, y, z). | 
| XMLsightingData_citiesUSA07.xml | Contains data pertaining to ISS sighting times. Contains the locations of sightings within a part of the United States (in the combinations of city, state, country), with information regarding the time and location in the sky the ISS is visible in. | 

These datasets and more are available on the [NASA Data Portal](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq). 

## Running the API
In order to run this API, Docker must be installed and running in the background.

To run the Flask server, do the following: 
1. Download the repository. This can be done through manually downloading the project files or by cloning the repository.
2. Navigate to the API directory in the terminal.
3. In the terminal, run the `make` command.

The server should be up and running. Navigate to `localhost:5000` to confirm that the server has been set up properly.

## Using the API
The datasets are accessed through the browser. This API can query the data files in several ways. To query the API, perform the following:
1. Ensure the API is running. Run `docker ps` in the terminal to check if the server is up.
   If the server is not up, run `docker images | grep nasa-api` in the terminal. If nothing appears, repeat the instructions in the Running the API section. 
2. Run `docker start nasa-api`. The Flask server should run in the terminal.
3. Use the terminal to send a POST request to the `/load-data` endpoint on the server. For example, `curl -X POST localhost:5000/load-data`. This will load the data from the data files.
4. Use one of the endpoints below to query the data set or return to `localhost:5000` for additional information about each endpoint.

| Endpoint | Result |
| - | - | 
| `/` | Main endpoint. Contains information regarding all other endpoints in this API |
| `/load-data` | Loads data from local files into the database. |
| `/epoch` | Retrieves all epochs in positional data. |
| `/epoch=<epoch>` | Retrieves specific epoch with specific flight time. Epoch must be a string. | 
| `/countries` | Retrieves all countries in sighting data. |
| `/countries=<country>` | Retrieves all entries in a specific country in sighting data. Country must be a string and encapsulated in quotation marks. | 
| `/countries=<country>/regions` | Retrieves all regions within a country in sighting data. Country must be a string. |
| `/countries=<country>/regions=<region>` | Retrieves all entries in a specific region witin a country in sighting data. Country and region must be a string. |
| `/countries=<country>/regions/cities` | Retrieves all cities in sighting data specified country and region. Country and region must be strings. |
| `/countries=<country>/regions=<region>/cities=<city>` | Retrieves all entries about a specific city in a specified country and region sighting data. Country, region, and city must be a string. |

All strings must be encapsulated in quotation marks like so: `localhost:5000/countries="United_States"`. 
Note: The `/epoch=<epoch>` endpoint is an exception to this. Use it like so `localhost:5000/epoch=EPOCHTIMESTAMP`. 

## How to Contribute
To contribute to this repository:
1. Fork this repository.
2. Send a pull request.
