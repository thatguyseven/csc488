#!/usr/bin/env python3 
import xmltodict  # Import xmltodict to convert XML into a Python dictionary
import pandas as pd  # Import pandas for data handling
from datetime import datetime  # Import datetime for time formatting


def show_Epochs(list_of_flight_data, epoch_key):
    """
    Iteratates through a list of ISS flight data, pulling out values associated with a given key and prints out each unique epoch.
    An epoch is determined by unique timestamps

    Args:
         list_of_flight_data (dict): A list of dictionaries. For passing ISS flight data.
         epoch_key (string): String key to access specific elements
    
    Returns:
        epochs (list): A list of all unique epochs identified
    """
    epochs = []
    for row in list_of_flight_data:
        curr_Epoch = row[epoch_key]
        if curr_Epoch not in epochs:
            epochs.append(curr_Epoch)
    return(epochs)

def find_Epoch(list_of_flight_data, x, y, z):
    """
    Uses positional data to return all data about an Epoch. Iterates through the flight data list and matches the x, y, z coordinate arguments.

	Parameters: 
        list_of_flight_data (dict): A list of dictionaries. For passing ISS flight data.
        x (float): The x coordinate of ISS flight.
        y (float): The y coordinate of ISS flight.
        z (float): The z coordinate of ISS flight.
	Return: 
        epoch (dict): Returns the row which the flight data coordinates.
    """
    for epoch in list_of_flight_data:
        if (epoch["x"] == x) and (epoch["y"] == y) and (epoch["z"] == z):
            return(epoch)
    return ({})

def main():
    # ---- STEP 1: Read and Parse XML File ----
    file_path = "/code/data/ISS.OEM_J2K_EPH.xml"  # Define the path to the XML file

    # Open and read the XML file
    with open(file_path, "r", encoding="utf-8") as file:
        xml_data = file.read()  # Read the entire XML content

    # Convert XML to a Python dictionary
    data_dict = xmltodict.parse(xml_data)

    # ---- STEP 2: Extract Metadata ----
    # Navigate to metadata (header information)
    metadata = data_dict["ndm"]["oem"]["header"]  # Access the <header> section
    print("Metadata:", metadata)  # Print metadata

    # ---- STEP 3: Extract State Vector Data ----
    ephemeris_data = []  # List to store parsed ephemeris data

    # Navigate to the list of <stateVector> elements
    state_vectors = data_dict["ndm"]["oem"]["body"]["segment"]["data"]["stateVector"]

    # Loop through each <stateVector> entry and extract data
    for state_vector in state_vectors:
        epoch = state_vector["EPOCH"]  # Extract timestamp

                # Extract position coordinates (handle nested dictionary issue)
        x = float(state_vector["X"]["#text"]) if isinstance(state_vector["X"], dict) else float(state_vector["X"])
        y = float(state_vector["Y"]["#text"]) if isinstance(state_vector["Y"], dict) else float(state_vector["Y"])
        z = float(state_vector["Z"]["#text"]) if isinstance(state_vector["Z"], dict) else float(state_vector["Z"])

        # Extract velocity components (handle nested dictionary issue)
        x_dot = float(state_vector["X_DOT"]["#text"]) if isinstance(state_vector["X_DOT"], dict) else float(state_vector["X_DOT"])
        y_dot = float(state_vector["Y_DOT"]["#text"]) if isinstance(state_vector["Y_DOT"], dict) else float(state_vector["Y_DOT"])
        z_dot = float(state_vector["Z_DOT"]["#text"]) if isinstance(state_vector["Z_DOT"], dict) else float(state_vector["Z_DOT"])

        # Append data as a dictionary to the list
        ephemeris_data.append({
            "epoch": epoch,
            "x": x, "y": y, "z": z,
            "vx": x_dot, "vy": y_dot, "vz": z_dot
        })

    # ---- STEP 4: Convert to Pandas DataFrame ----
    df = pd.DataFrame(ephemeris_data)  # Convert list to DataFrame

    # Convert 'epoch' column from string to datetime format
    df["epoch"] = pd.to_datetime(df["epoch"], format="%Y-%jT%H:%M:%S.%fZ")

    # Display first few rows of the DataFrame
    print("\nEphemeris Data as DataFrame:")
    print(df.head())

    epochs = show_Epochs(ephemeris_data, "epoch")
    for epoch in epochs:
        print(epoch)

if __name__ == '__main__': 
    main()