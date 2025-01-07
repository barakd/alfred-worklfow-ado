import os


def get_projects():
    rawProjects = os.getenv('ado_projects')
    projects = rawProjects.split(',')
    return projects

def get_projects_for_pipelines():
    projects = get_projects()
    projects_to_exclude = os.getenv('projects_exclude_pipelines')
    if(projects_to_exclude is not None):
        projects_to_exclude = projects_to_exclude.split(',')
        projects = [project for project in projects if project not in projects_to_exclude]
    return projects

def get_pulls_requets_project_and_critera():
    projects = get_projects()
    projectsToExclude = os.getenv('projects_exclude_prs')
    if(projectsToExclude is not None):
        projectsToExclude = projectsToExclude.split(',')
        projects = [project for project in projects if project not in projectsToExclude]
    createdByIds = os.getenv('ado_created_by_id').split(',') if os.getenv('ado_created_by_id') else []
    reviewersIds = os.getenv('prs_with_reviewers_by_ids').split(',') if os.getenv('prs_with_reviewers_by_ids') else []
    tuples = []
    for project in projects:
        for createdById in createdByIds:
            tuples.append((project, createdById, 'creatorId'))
        for reviewersId in reviewersIds:
            tuples.append((project, reviewersId, 'reviewerId'))
    return tuples