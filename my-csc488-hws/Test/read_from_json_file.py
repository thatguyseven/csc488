import json

def read_from_json_file(filename):
    # Attempt to read from 
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError: 
        print(f"Error: The file '{filename}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' does not contain valid JSON.")
        return None
    
data = read_from_json_file("test.json")

print(data)