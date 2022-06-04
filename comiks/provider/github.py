import requests

from comiks.model import Repository
from comiks.provider.base import Provider


class GithubProvider(Provider):

    name = 'Github'
    tags = ['github']

    def get_repositories(self, username):
        raw = requests.get(f'https://api.github.com/users/{username}/repos').json()
        return [
            Repository(repo['name'], repo['html_url'])
            for repo in raw
        ]
