
from github import Github
from github import Auth
import github.Tag as Tag

from env import Env

def get_latest_central_version():
    '''
    output: -> Tag : latest tag for central
    '''
    organisation = github.get_organization("discovery-ltd")
    central_repo = organisation.get_repo("v1-gutenberg-central-app-flutter")
    updated_tag = central_repo.get_tags()[0]

    return updated_tag

def get_tenant(tenant_number):
    '''
    input:
        tenant_number -> int : tenant number 

    output: -> Repository : tenant repository
    '''
    organisation = github.get_organization("discovery-ltd")
    tenant_repo = organisation.get_repo("v1-tenant-{}-flutter".format(tenant_number))
    
    return tenant_repo


def build_release_yaml(release_file, update_tag):
    '''
    input:
        release_file -> str : content of the present release.yaml
        update_tag -> str : latest tag on central

    output: -> str: updated release.yaml
    '''
    updated_yaml = ""
    for line in release_file.splitlines():
        if("version" in line):
            new_line = "    version: " + update_tag
            updated_yaml = release_file.replace(line, new_line, 1)
            break

    return updated_yaml

def get_current_host_app_version(release_file):
    '''
    input: 
        release_file -> str: content of the present release.yaml
    output: -> str: current tag of host app on release.yaml
    '''
    current_tag = ""
    for line in release_file.splitlines():
        if("version" in line):
            current_tag = line.split(":")[1].strip()
            break

    return current_tag

def create_new_branch(repo, from_branch, target_branch):
    '''
    input:
        repo -> Repository: repository object
        from_branch -> str: branch name to be used for base
        target_branch -> str: branch name that needs to be created
    '''
    source_branch = repo.get_branch(from_branch)
    repo.create_git_ref(ref="refs/heads/"+target_branch, sha=source_branch.commit.sha)
    print("new branch created: ", target_branch)


def delete_branch(repo, target_branch):
    '''
    input:
        repo -> Repository: repository object
        target_branch -> str: branch name that needs to be deleted
    '''
    if(target_branch in [branch.name for branch in list(repo.get_branches())]):
        print(target_branch, "found, deleting...")
        repo.get_git_ref(ref="heads/" + target_branch).delete()

def is_pr_available_for(repo, pr_title):
    '''
    tells you if the PR you're trying to raise already exists or not

    input:
        repo -> Repository: repository object
        pr_title -> str: PR title that you're trying to raise the PR for
    output: -> bool
    '''
    for pr in repo.get_pulls():
        if(pr_title in pr.title):
            print("similar pr already exists")
            return True
    print("no previous pr found")
    return False

def update_for_tenant(tenant_number: int, latest_central_tag: Tag):
    '''
    updates tenant repository with the latest central version

    input:
        tenant_number -> int: tenant number
    '''
    target_branch = "update_app_host"
    tenant = get_tenant(tenant_number)

    release_yaml = tenant.get_contents("release.yaml")
    release_yaml_content = release_yaml.decoded_content.decode()
    current_tag = get_current_host_app_version(release_yaml_content)

    print("current tag:", current_tag)
    print("updated tag:", latest_central_tag.name)

    if(current_tag != latest_central_tag.name and not is_pr_available_for(tenant, pr_title)):
        # delete branch if exists
        delete_branch(tenant, target_branch)
        # create new branch
        create_new_branch(tenant, "master", target_branch)
        # update the file
        updated_yaml = build_release_yaml(release_yaml_content, latest_central_tag.name)
        # create a commit
        tenant.update_file(release_yaml.path, commit_title, updated_yaml, release_yaml.sha, branch=target_branch)
        # create a PR
        tenant.create_pull(base="master", head=target_branch, title=pr_title, body="")

def update_tenants(tenant_list: list, latest_central_tag: Tag):
    '''
    updates multiple tenants with the latest central version

    input:
        tenant_list -> list<int>: list of tenant numbers
    '''

    for tenant in tenant_list:
        try:
            update_for_tenant(tenant, latest_central_tag)
        except Exception as e:
            print("error updating tenant: ", tenant)
            print(e)




if(__name__ == "__main__"):
    # authentication
    auth = Auth.Token(Env.github_token)
    github = Github(auth=auth)

    # get latest central version
    latest_central_tag = get_latest_central_version()
    
    pr_title = "[{}]: update host app version to {}".format(Env.ticket_number, latest_central_tag.name)
    commit_title = "[{}]: update host app version to {}".format(Env.ticket_number, latest_central_tag.name)
    
    update_tenants([25], latest_central_tag)
    
    github.close()

