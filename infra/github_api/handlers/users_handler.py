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
            gists.append(Gist.from_github(gist))

        return gists
