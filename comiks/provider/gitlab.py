'''GitLab provider.'''

import requests

from comiks.exceptions import AuthException, NotFoundException
from comiks.model import UserInfos, Repository
from comiks.provider.base import Provider


class GitlabProvider(Provider):
    '''Get user infos and repositories from GitLab provider.'''

    name = 'GitLab'
    url = 'gitlab.com'
    tags = ['gitlab']

    def __get(self, endpoint, params=None):
        resp = requests.get(
            f'https://gitlab.com/api/v4{endpoint}',
            params=params or {},
            headers={
                'PRIVATE-TOKEN': self.config['access_token'],
            }
        )

        if resp.status_code == 401:
            raise AuthException()

        return resp.json()

    def get_user_infos(self, username):
        resp = self.__get('/users', {'username': username})

        if len(resp) == 0:
            raise NotFoundException()

        return UserInfos(
            username=resp[0]['username'],
            display_name=resp[0]['name'],
            identifier=resp[0]['id'],
        )

    def get_repositories(self, user_infos):
        # Get events with action created
        events = self.__get(f'/users/{user_infos.identifier}/events?action=created')
        project_ids = [event['project_id'] for event in events]
        # Get events with action joined
        events = self.__get(f'/users/{user_infos.identifier}/events?action=joined')
        project_ids.extend([event['project_id'] for event in events])
        # Get name and URL for each project
        for project_id in project_ids:
            project = self.__get(f'/projects/{project_id}')
            yield Repository(project['name_with_namespace'], project['http_url_to_repo'])
