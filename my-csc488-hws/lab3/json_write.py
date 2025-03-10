import json 
 
data = {} 
data['class'] = 'CSC488' 
data['title'] = 'Principles of Distributed Software Systems' 
data['subjects'] = [] 
data['subjects'].append( {'unit': 1, 'topic': ['linux', 'python3', 'git']} ) 
data['subjects'].append( {'unit': 2, 'topic': ['json', 'csv', 'xml', 'yaml']} ) 
 
with open('class.json', 'w') as out: 
    json.dump(data, out, indent=2) 
