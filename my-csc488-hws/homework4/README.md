# Homework 4
The app `ml_data_analysis.py` is ready to be released to the world, so it is time to create a container so that others can use this application. 

## Task
In this assignment, the application `ml_data_analysis.py` is containerized and published to the public repo.

## Contents
| File | Description | 
| - | - |
| `ml_data_analysis.py` | A python script that analyzes meteority landing site data from a JSON file and determines the number of sites in each hemisphere. |
| `test_ml_data_analysis.py` | A pytest script that tests `ml_data_analysis.py` to ensure `ml_data_analysis.py` is functioning properly. | 
| `Dockerfile` | Dockerfile for building `ml_data_analysis.py` as a container. |
| `Dockerfile_test` | Dockerfile for building `test_ml_data_analysis.py` as a container. |
| `Makefile` | Makefile for building and publishing both app and testing containers and pushing them to your public repository. |

# Run Instructions
Below are instruction for how to get and run the app as a container.

## Pulling the Existing Image
To pull a copy of the existing container:
1. Open your terminal.
2. Run the following commands to download the respoective container:
   `docker pull aan1/quadrant-landings` -> Application Container
   `docker pull aan1/test-quadrant-landings` -> Test Container

## Building the Container
To buils a new container and push it to your own repository:
1. Download the contents of this folder.
2. Open your terminal.
3. Navigate to the folder containing all of the application files.
4. Change the `Name` variable in the Makefile to your username.
5. Run the `make` command to build both containers or run one of the following commands to build the respective container:
   `docker build -f ./Dockerfile -t ${Name}/quadrant-landings:latest .` -> Application Container
   `docker build -f ./Dockerfile_test -t ${Name}/test-quadrant-landings:latest .` -> Test Container

## Running the Code
To pull a copy of the existing container:
1. Open your terminal.
2. Run the command to run the container:
   `docker run --rm  <username>/quadrant-landings:latest` -> Application Container
   If you want to use your own JSON file, run the following command:
   `docker run --rm -v ${PWD}:/data <username>/quadrant-landings:latest /data/<filename>`

If you need a sample dataset to try the above command, there is one available [here](https://raw.githubusercontent.com/wjallen/coe332-sample-data/main/ML_Data_Sample.json).

## Testing the App
To test the application, run `docker run --rm  <username>aan1/test-quadrant-landings:latest`.
