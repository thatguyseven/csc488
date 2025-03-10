import xmltodict 
 
data = {} 
data['class'] = 'CSC488' 
data['title'] = 'Principle of Distributed Software Systems' 
data['subjects'] = [] 
data['subjects'].append( {'unit': 1, 'topic': ['linux', 'python3', 'git']} ) 
data['subjects'].append( {'unit': 2, 'topic': ['json', 'csv', 'xml', 'yaml']} ) 
 
root = {} 
root['data'] = data 
 
with open('class.xml', 'w') as o: 
    o.write(xmltodict.unparse(root, pretty=True)) 
