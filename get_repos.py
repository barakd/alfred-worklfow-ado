#!/usr/bin/env python3
import json
from src.configurationHelper import get_projects
from src.adoClient import api_call

cache_duration = 86400  # 24 hours in seconds
projects = get_projects()

def list_repos_of_project(proj):
    repos = api_call('GET', f'/{proj}/_apis/git/repositories?api-version=7.1')
    items = []
    for repo in repos:
            item = {
                "uid": repo["id"],
                "type": "url",
                "title": repo["name"],
                "subtitle": repo["description"] if "description" in repo else "",
                "arg": repo["webUrl"],
                "autocomplete": repo["name"],
            }
            items.append(item)
    result = items
    return result

def get_repos():
    repos = []
    for project in projects:
        repos.extend(list_repos_of_project(project))

    repositoriesResponse = {"items": repos, "cache": { "seconds" : cache_duration }} 
    return repositoriesResponse
    
def main():
    try:
        repos = get_repos()
        print(json.dumps(repos, indent=4))
        
    except Exception as error:
        print(f'Error: {error}')

main()