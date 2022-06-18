'''GitHub provider.'''

import requests

from comiks.exceptions import AuthException, NotFoundException
from comiks.model import UserInfos, Repository
from comiks.provider.base import Provider


class GithubProvider(Provider):
    '''Get user infos and repositories from GitHub provider.'''

    name = 'GitHub'
    url = 'github.com'
    tags = ['github']

    def __get(self, endpoint, params=None):
        resp = requests.get(
            f'https://api.github.com{endpoint}',
            params=params or {},
            auth=(
                self.config.get('username'),
                self.config.get('access_token'),
            )
        )

        if resp.status_code == 401:
            raise AuthException()

        return resp.json()

    def get_user_infos(self, username):
        resp = self.__get(f'/users/{username}')

        if resp.get('message') == 'Not Found':
            raise NotFoundException()

        return UserInfos(
            username=resp['login'],
            display_name=resp['name'],
            identifier=resp['id'],
        )

    def get_repositories(self, user_infos):
        repos = self.__get(f'/users/{user_infos.username}/repos')
        for repo in repos:
            yield Repository(
                name=repo['name'],
                url=repo['html_url'],
                fork=repo['fork'],
            )
