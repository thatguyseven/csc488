import json
import random

def generate_latitude():
    return round(random.uniform(16.0, 18.0), 10)

def generate_longitude():
    return round(random.uniform(82.0, 84.0), 10)

def generate_composition():
    composition_types = ['stony', 'iron', 'stony-iron']
    rand_comp =  random.randint(0, 2)
    return composition_types[rand_comp] # returns the randomly selected composition type

def generate_sites(num_of_sites):
    sites = {}
    sites['sites'] = []

    for i in range(num_of_sites):
        site_id = i+1
        # generate random values for site data
        lat = generate_latitude();
        lon = generate_longitude();
        comp = generate_composition();
        sites['sites'].append( {'site_id': site_id, 'latitude': lat, 'longitude': lon, 'composition': comp} )          # appends generated values to list
    with open('sites.json','w') as out:
         json.dump(sites, out, indent=2)

generate_sites(5) 
