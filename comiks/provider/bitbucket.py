'''Bitbucket provider.'''

import requests

from comiks.exceptions import AuthException, NotFoundException
from comiks.model import UserInfos, Repository
from comiks.provider.base import Provider


class BitbucketProvider(Provider):
    '''Get user infos and repositories from Bitbucket provider.'''

    name = 'Bitbucket'
    url = 'bitbucket.org'
    tags = ['bitbucket']

    def __get(self, endpoint, params=None, paginated=False):
        results = []
        params = params or {}

        page = 1
        while True:
            if paginated:
                params['page'] = page

            resp = requests.get(
                f'https://bitbucket.org/api/2.0{endpoint}',
                params=params,
                auth=(
                    self.config.get('username'),
                    self.config.get('app_password'),
                ),
            )
            if resp.status_code == 401:
                raise AuthException()

            data = resp.json()

            if not paginated:
                results = data
                break

            results.extend(data['values'])

            if len(results) >= data['size']:
                break

            page += 1

        return results

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
        repos = self.__get(f'/repositories/{user_infos.username}', paginated=True)
        for repo in repos:
            if repo['type'] == 'repository':
                repo_name = ' / '.join(repo['full_name'].split('/'))
                repo_url = [
                    link['href']
                    for link in repo['links']['clone']
                    if link['name'] == 'https'
                ][0]
                yield Repository(
                    name=repo_name,
                    url=repo_url,
                    fork=repo.get('parent', False),
                )
