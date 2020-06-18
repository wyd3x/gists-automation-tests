import requests

from infra.github_api.consts.http_method import HTTPMethod
from infra.github_api.consts.routes import USERS_ROUTE
from infra.models.gist import Gist


class UsersHandler:
    def __init__(self,
                 github_conn):
        self.github_conn = github_conn

    def get_gists(self, username: str) -> [Gist]:
        response = self.github_conn.request(method=HTTPMethod.get, url=f'{USERS_ROUTE}/{username}/gists')
        gists = []
        for gist in response.get('body'):
            for file in gist.get('files'):
                file_data = gist.get('files')[file]
                file_data['content'] = requests.get(url=file_data.get('raw_url')).text
            gists.append(Gist.from_github(gist))

        return gists
