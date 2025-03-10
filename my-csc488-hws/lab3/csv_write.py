import csv 
import json 
 
data = {} 
 
with open('Meteorite_Landings.json', 'r') as f: 
    data = json.load(f) 
 
with open('Meteorite_Landings.csv', 'w') as o: 
    csv_dict_writer = csv.DictWriter(o, data['meteorite_landings'][0].keys()) 
    csv_dict_writer.writeheader() 
    csv_dict_writer.writerows(data['meteorite_landings']) 
