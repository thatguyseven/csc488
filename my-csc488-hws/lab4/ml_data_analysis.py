#!/usr/bin/env python3

import json 
from typing import List
"""
Logging Setup
"""

import logging
import socket
format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(lineno)s - %(levelname)s: %(message)s'

logging.basicConfig(level=logging.DEBUG, format=format_str)    # configs the logging instance

def compute_average_mass(a_list_of_dicts, a_key_string) -> float:
    """
    Iteratates through a list of dictionaries, pulling out values associated with a given key. Returns the average of those values.

    Args:
         a_list_of_dicts (list): A list of dictionaries, each dict should have the same set of keys.
         a_key_string (string): A key that appears in each dictionary associated with the desired value (will enforce float type).
    
    Returns:
        result (float): Average value.
    """

    total_mass = 0.
    
    for item in a_list_of_dicts:
        total_mass += float(item[a_key_string])
    
    # logging.debug(f'{total_mass / len(a_list_of_dicts)}')    # DEBUG: prints the result
    return(total_mass / len(a_list_of_dicts) )


def check_hemisphere(latitude, longitude) -> float:
    """
    Given latitude and longitude in decimal notation, returns which hemispheres those coordinates land in.

    Args: 
        latitude (float): Latitude in decimal notation.
        longitude (float): Longitude in decimal notation.

    Returns: 
        location (string): Short string listing two hemispheres.
    """

    location = 'Northern' if (latitude > 0) else 'Southern'
    location = f'{location} & Eastern' if (longitude > 0) else f'{location} & Western'
    
    # logging.debug(f'{location}')    # DEBUG: Prints output location.
    return(location)

def count_classes(list_of_dicts, class_key) -> List:
    """
    Given a list of dictionaries and a class key, iterates through the list of dictionaries, counting each instance of unique values. Returns a list with unique values and a count of the number of instances found in the list of dictionaries.

    Args: 
        list_of_dicts (list): A list of dictionaries, each dict should have the same set of keys.
        class_key (string): A key that appears in each dictionary.

    Returns:
        class_dict (list): A list of dictionaries containing unique instances and a count of each instance.
    """

    class_dict = {}
    for item in list_of_dicts:
        recclass = item[class_key]
        if recclass in class_dict:
            class_dict[recclass] += 1
        else:
            class_dict[recclass] = 1
            # logging.debug(f'{recclass} added!')    # DEBUG: Prints when a unique class is discovered.
    
    return(class_dict)

def main(): 
    with open('Meteorite_Landings.json', 'r') as f:
        ml_data = json.load(f)
    
    print(compute_average_mass(ml_data['meteorite_landings'] ,'mass (g)' ))

    for row in ml_data['meteorite_landings']:
        print(check_hemisphere(float(row['reclat']), float(row['reclong'])))
    

    dict_of_classes = count_classes(ml_data['meteorite_landings'], 'recclass')
    for recclass in dict_of_classes:
        print(f"{recclass}:", dict_of_classes[recclass])

if __name__ == '__main__': 
    main()
