#!/usr/bin/env python3 
import requests

"""
Functions:
    retrieve_org_api(org_id): Returns org_dict which contains all metadata as a dict
    retrieve_members(org_id): Returns member_list which contains all member login attributes
    retrieve_repos(org_id): Returns repo_list which contains all repositories full_name attributes
"""

def retrieve_org_api(org_id):
    api_response = requests.get(url=f"https://api.github.com/orgs/{org_id}")

    meta_data = api_response.json()
    return meta_data


def retrieve_members(org_id):
    api_response = requests.get(url=f"https://api.github.com/orgs/{org_id}/members")

    meta_data = api_response.json()
    member_list = []
    for member in meta_data:
        member_list.append(member["login"])

    return member_list

def retrieve_repos(org_id):
    api_response = requests.get(url=f"https://api.github.com/orgs/{org_id}/repos")

    meta_data = api_response.json()
    repo_list = []
    for repository in meta_data:
        repo_list.append(repository["full_name"])

    return repo_list

print("\nRetrieving metadata from \"TACC\" GitHub API")
data = retrieve_org_api("TACC")
print(data)

print("\nRetrieving member logins from \"TACC\" GitHub API")
data = retrieve_members("TACC")
for line in data: print(line)

print("\nRetrieving repository names from \"TACC\" GitHub API")
data = retrieve_repos("TACC")
for line in data: print(line)