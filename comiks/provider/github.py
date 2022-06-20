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
        # Get repositories listed in user account
        repos = self.__get(f'/users/{user_infos.username}/repos')
        repos_map = {
            repo['id']: repo
            for repo in repos
        }
        # Find repositories the user has contributed to, but that
        # are not listed in user account
        commits = self.__get(f'/search/commits?q=author-name:{user_infos.username}')
        for commit in commits['items']:
            repo = commit['repository']
            repos_map[repo['id']] = repo

        for repo in repos_map.values():
            yield Repository(
                name=repo['name'],
                url=repo['html_url'],
                fork=repo['fork'],
            )
