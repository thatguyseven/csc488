import json 
 
with open('Meteorite_Landings.json', 'r') as f: 
    ml_data = json.load(f)

type(ml_data) 
type(ml_data['meteorite_landings']) 
type(ml_data['meteorite_landings'][0]) 
type(ml_data['meteorite_landings'][0]['name']) 
 
print(ml_data) 
print(ml_data['meteorite_landings']) 
print(ml_data['meteorite_landings'][0]) 
print(ml_data['meteorite_landings'][0]['name']) 
