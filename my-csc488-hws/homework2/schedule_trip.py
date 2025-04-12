import math
import json

def great_circle_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Radius of Mars in kilometers (mean radius)
    R = 3389.5

    # Calculate the distance
    distance = R * c

    return distance/10

def gather_sample(comp):
    composition_type = {'stony':1, 'iron':2, 'stony-iron':3}

    return composition_type[comp]

def calculate_trip(list_of_sites): 
    location = {'latitude': 16.0, 'longitude': 82.0}
    num_trips = 0
    total_time = 0
    
    for site in list_of_sites:
        site_num = site['site_id']
        trip_time = great_circle_distance(location['latitude'],location['longitude'], site['latitude'], site['longitude'])
        sample_time = gather_sample(site['composition'])
        num_trips += 1
        total_time += trip_time + sample_time
        print(f'dest = {site_num}, travel time = {trip_time}, sample time = {sample_time}')

    print('==================================')
    print(f'number of trips = {num_trips}, total time elapsed = {total_time}')

with open('sites.json', 'r') as f: 
    sites = json.load(f)

calculate_trip(sites['sites']) 
