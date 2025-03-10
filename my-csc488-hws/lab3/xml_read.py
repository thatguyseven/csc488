import xmltodict 

with open('Meteorite_Landings.xml', 'r') as f: 
    data = xmltodict.parse(f.read()) 

print(data['data']['meteorite_landings'][0])

