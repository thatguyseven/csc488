import json

data = {
    "name": "Alice",
    "age": 25,
    "city": "New York",
    "skills": ["Python", "Flask", "Docker"]
}

data["skills"].append("Kubernetes")

print(data)

def save_to_json_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

save_to_json_file(data, "test.json")