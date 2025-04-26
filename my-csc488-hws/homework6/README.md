# Homework 6
This directory contains a Kubernetes deployment of the Flask app present in Lab 7. This application deploys the API in a Kubernetes cluster.

Prerequisites:
- Docker.
- Redis Database.
- Directory files.
- Meteorite_Landings.json file. This dataset is available [here](https://raw.githubusercontent.com/wjallen/coe332-sample-data/main/ML_Data_Sample.json).
- A Kubernetes Cloud or a comparable container. MiniKube is used in this application.

Contents:
| File | Description |
| - | - |
| redis_info.py | An import file for returning a Redis database address from the localhost. |
| app.py | A copy of app.py from Lab 6 with an added `/data` endpoint. |
| requirements.txt | A text file containing the python dependencies required for this application. |
| Dockerfile | Dockerfile to build the Flask application. |
| Makefile | Makefile to simplify building process. |

## Building the App
To run the app, follow the instructions below.
1. Download the application files.
2. In the terminal, change to the directory containing the application files.
3. Within the Makefile, change the `Name` variable to match your Docker username.
4. Run `minikube start` to launch the Kubernetes cloud server. This step can be skipped if already connected to a Kubernetes cloud server.
5. Build the image with the command: `make`. This will build the image.

The cluster should be available now. To verify, follow the instructions below:
1. In the terminal, run `kubectl get pods`. Three pods should be running.
2. Run `kubectl get services` to check that the services are running. The services `test-flask-server` and `test-redis-server` should exist.

## Application Endpoints
The following endpoints are available:

| Endpoint | Request Type | Description | Options |
| - | - | - | - |
| `/data` | POST | Loads site data in `Meteorite_Landings.json` into Redis database. | None |
| `/data` | GET | Retrieves site data from the Redis database. | limit - Limits number of entries retrieved, starting from the first |

To test these endpoints, open a python debug environment to `curl` the server by following the instructions below:
1. In the command line, run `kubectl apply -f deployments/deployment-python-debug.yml`.
2. Run `kubectl get services`. Note down the IP address of the Flask server.
3. In a separate terminal, run `kubectl exec -it py-debug-deployment-6c86744b9b-hpdv9 -n default -- /bin/sh` to open the command line for the test evironment.
4. In the python debug environment, run `curl -X POST <your-flask-ip-addr>:5000/data`. This will load the data into the redis server.
5. In the python debug environment, run `curl <your-flask-ip-addr>:5000/data`. This will output data points from the server.

## Interpretting the Data
The meteorite landing data returned contains the following:
- name - The name of the landing site
- id - The specific site ID
- recclass - The class of meteorite
- mass (g) - The mass of the meteorite in grams
- reclat - The latitudinal coordinate of the landing site
- reclong - The longitudinal coordinate of the landing site
- Geolocation - The geolocation coordinates of the landing site
