# Homework 7

This directory contains a dataflow diagram of the POST endpoint. 

## Explanation
The included diagram shows the data flow of the POST endpoint for the ISS Data API.

The endpoints functions as follows:
1. The POST endpoint begins with a POST request with two optional inputs: `positional_file` and `sighting_file`. These two optional inputs determine the file the data is saved to. 
2. The API then checks whether the file exists. This is meant for first runs of the API and unique sample data files. The data is then saved in the specified file(s) and stored in local program memory as a Pandas Dataframe.
3. The API then returns a success message based on the success of the process.
