#!/usr/bin/env python3
import json

from src.configurationHelper import get_projects_for_pipelines
from src.adoClient import api_call

cache_duration = 60 * 60 * 24  # 1 hour
projects = get_projects_for_pipelines()

def fetch_pipelines(proj):
    pipeLines = api_call('GET', f'/{proj}/_apis/pipelines?api-version=7.1')
    items = []
    for pipe in pipeLines:
            item = {
                "uid": pipe["id"],
                "type": "action",
                "title": pipe["name"],
                "subtitle": pipe["folder"],
                "arg": pipe["id"],
                "autocomplete": pipe["name"],
            }
            items.append(item)
    return items

def main():
    try:
        pipelines = []
        for project in projects:
            pipelines.extend(fetch_pipelines(project))
        print(json.dumps({"items": pipelines, "cache": { "seconds" : cache_duration }} , indent=4))
    except Exception as error:
        print(f'Error: {error}')

main()