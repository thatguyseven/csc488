# Homework 5
This directory contains a containerized version of the Flask app present in Lab 7. This application allows for loading and querying the database immediately after building the application.

Prerequisites:
- Docker
- Redis Database
- Directory files

## Launching the Redis Database
To create the Redis database, run the command `docker run -d -p 6379:6379 -v ${pwd}:/data --name=hw5-data redis:6 --save 1 1`.

## Building the App
To run the app, follow the instructions below.
1. Download the application files.
2. In the terminal, change to the directory containing the application files.
3. Build the image with the command: `docker build -t <username>/hw5-data:latest .`
5. Run a container with the command: `docker run -d --name hw5-app -p 5000:5000 --link hw5-data:redis aan1/hw5-app:latest`

The Flask server should be up and running at this point.

## Application Endpoints
The following endpoints are available:

| Endpoint | Request Type | Description | Options |
| - | - | - | 
| `/data` | POST | Loads site data in `Meteorite_Landings.json` into Redis database. | None |
| `/data` | GET | Retrieves site data from the Redis database. | limit - Limits number of entries retrieved, starting from the first |

## Interpretting the Data
The meteorite landing data returned contains the following:
- name - The name of the landing site
- id - The specific site ID
- recclass - The class of meteorite
- mass (g) - The mass of the meteorite in grams
- reclat - The latitudinal coordinate of the landing site
- reclong - The longitudinal coordinate of the landing site
- Geolocation - The geolocation coordinates of the landing site
