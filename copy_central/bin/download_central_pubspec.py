from github import Github
from github import Auth

from env import Env

def download_file(repo: str, file_path: str, output_path: str):
    '''
    downloads file from any repo from the discovery-ltd organisation
    '''
    organisation = github.get_organization("discovery-ltd")
    central_repo = organisation.get_repo(repo)
    release_yaml = central_repo.get_contents(file_path)

    with open(output_path, "w") as file:
        file.write(release_yaml.decoded_content.decode())    

auth = Auth.Token(Env.github_token)
github = Github(auth=auth)

download_file(Env.remote_repo_name, Env.remote_file_path, Env.output_file_path)