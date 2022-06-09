import requests

from comiks.exceptions import AuthException, NotFoundException
from comiks.model import UserInfos, Repository
from comiks.provider.base import Provider


class BitbucketProvider(Provider):

    name = 'Bitbucket'
    url = 'bitbucket.org'
    tags = ['bitbucket']

    def __get(self, endpoint, params=None):
        resp = requests.get(
            f'https://bitbucket.org/api/2.0{endpoint}',
            params=params or {},
            auth=(
                self.config.get('username'),
                self.config.get('app_password'),
            ),
        )

        if resp.status_code == 401:
            raise AuthException()

        return resp.json()

    def get_user_infos(self, username):
        resp = self.__get(f'/workspaces/{username}')

        if resp.get('type') == 'error':
            raise NotFoundException()

        return UserInfos(
            username=resp['slug'],
            display_name=resp['name'],
            identifier=resp['uuid'],
        )

    def get_repositories(self, user_infos):
        repos = self.__get(f'/repositories/{user_infos.username}')
        for repo in repos.get('values', []):
            if repo['type'] == 'repository':
                repo_name = ' / '.join(repo['full_name'].split('/'))
                repo_url = [
                    link['href']
                    for link in repo['links']['clone']
                    if link['name'] == 'https'
                ][0]
                yield Repository(repo_name, repo_url)
