#!/usr/bin/ python3 
import json 
import random 
import sys 
import names

NUM = 10 
CLASSES = ['CI1', 'CR2-an', 'CV3', 'EH4', 'H4', 'H5', 'H6', 'L5', 'L6', 'LL3-6', 'LL5'] 
 
def main(): 
 
    data = {'meteorite_landings': [{} for _ in range (NUM)]} 
    
    for i in range(NUM): 
        rand_lat = '{:.4f}'.format(random.uniform(-90.0000, 90.0000)) 
        rand_lon = '{:.4f}'.format(random.uniform(-90.0000, 90.0000)) 
        data['meteorite_landings'][i]['name'] = names.get_first_name() 
        data['meteorite_landings'][i]['id'] = str(10000 + 1 + i) 
        data['meteorite_landings'][i]['recclass'] = random.choice(CLASSES) 
        data['meteorite_landings'][i]['mass (g)'] = str(random.randrange(1, 10000)) 
        data['meteorite_landings'][i]['reclat'] = rand_lat 
        data['meteorite_landings'][i]['reclong'] = rand_lon 
        data['meteorite_landings'][i]['GeoLocation'] = f'({rand_lat}, {rand_lon})' 
    
    with open(sys.argv[1], 'w') as o: 
        json.dump(data, o, indent=2) 
        print(f'Data written to {sys.argv[1]}!') 
 
if __name__ == '__main__': 
    main() 