import csv 
 
data = {} 
data['meteorite_landings'] = [] 
 
with open('Meteorite_Landings.csv', 'r') as f: 
    reader = csv.DictReader(f) 
    for row in reader: 
        data['meteorite_landings'].append(dict(row)) 
