import requests

from comiks.model import UserInfos, Repository
from comiks.provider.base import Provider


class GithubProvider(Provider):

    name = 'GitHub'
    url = 'github.com'
    tags = ['github']

    def get_user_infos(self, username):
        resp = requests.get(f'https://api.github.com/users/{username}').json()
        return UserInfos(
            username=resp['login'],
            display_name=resp['name'],
            identifier=resp['id'],
        )

    def get_repositories(self, user_infos):
        resp = requests.get(f'https://api.github.com/users/{user_infos.username}/repos').json()
        return [
            Repository(repo['name'], repo['html_url'])
            for repo in resp
        ]
