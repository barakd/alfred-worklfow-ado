#!/usr/bin/env python3
import json
import os
from sys import argv

from src.configurationHelper import get_pulls_requets_project_and_critera
from src.adoClient import api_call

cache_duration = 60 * 60  # 1 hour
sourcesAndReviewersTuples = get_pulls_requets_project_and_critera()

def fetch_prs(proj, reviewer, creitera):
    prs = api_call('GET', f'/{proj}/_apis/git/pullrequests?searchCriteria.{creitera}={reviewer}&api-version=7.1')    
    items = []
    for pr in prs:
            project_name = pr["repository"]["project"]["name"]
            repo_name = pr["repository"]["name"]
            pull_request_id = pr["pullRequestId"]
            pr_url = f"https://microsoft.visualstudio.com/{project_name}/_git/{repo_name}/pullrequest/{pull_request_id}"
            item = {
                "uid": pr["pullRequestId"],
                "type": "url",
                "title": pr["title"],
                "subtitle": pr["description"] if "description" in pr else "",
                "arg": pr_url,
                "autocomplete": pr["title"],
            }
            items.append(item)
    result = items
    return result
    
def get_prs():
    prs = []
    for sourceAndReviewerTuple in sourcesAndReviewersTuples:
        prs.extend(fetch_prs(sourceAndReviewerTuple[0], sourceAndReviewerTuple[1],  sourceAndReviewerTuple[2]))

    prs_data = {"items": prs , "cache": { "seconds" : cache_duration }} 
    return prs_data


def main():
    try:
        prs = get_prs()
        print(json.dumps(prs, indent=4))
    except Exception as error:
        print(f'Error: {error}')

main()