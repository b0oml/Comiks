import requests

from comiks.model import UserInfos, Repository
from comiks.provider.base import Provider


class GithubProvider(Provider):

    name = 'GitHub'
    url = 'github.com'
    tags = ['github']

    def __get(self, endpoint, params=None):
        return requests.get(
            f'https://api.github.com{endpoint}',
            params=params or {},
            auth=(
                self.config.get('username'),
                self.config.get('access_token'),
            )
        ).json()

    def get_user_infos(self, username):
        resp = self.__get(f'/users/{username}')

        if resp.get('message') == 'Not Found':
            return None

        return UserInfos(
            username=resp['login'],
            display_name=resp['name'],
            identifier=resp['id'],
        )

    def get_repositories(self, user_infos):
        repos = self.__get(f'/users/{user_infos.username}/repos')
        for repo in repos:
            yield Repository(repo['name'], repo['html_url'])
