import requests

from comiks.model import UserInfos, Repository
from comiks.provider.base import Provider


class GitlabProvider(Provider):

    name = 'GitLab'
    url = 'gitlab.com'
    tags = ['gitlab']

    def __get(self, endpoint, params=None):
        return requests.get(
            f'https://gitlab.com/api/v4{endpoint}',
            params=params or {},
            headers={
                'PRIVATE-TOKEN': self.config['access_token'],
            }
        ).json()

    def get_user_infos(self, username):
        resp = self.__get('/users', {'username': username})
        return UserInfos(
            username=resp[0]['username'],
            display_name=resp[0]['name'],
            identifier=resp[0]['id'],
        )

    def get_repositories(self, user_infos):
        resp = self.__get(f'/users/{user_infos.identifier}/projects')
        return [
            Repository(repo['name'], repo['http_url_to_repo'])
            for repo in resp
        ]
