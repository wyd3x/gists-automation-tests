from infra.github_api.consts.http_method import HTTPMethod
from infra.github_api.consts.routes import GISTS_ROUTE
from infra.models.gist import Gist


class GistsHandler:
    def __init__(self,
                 github_conn):
        self.github_conn = github_conn

    def read(self, gist_id: str) -> ['Gist']:
        response = self.github_conn.request(method=HTTPMethod.get,
                                            url=f'{GISTS_ROUTE}/{gist_id}')

        return Gist.from_github(response.get('body'))

    def create(self, gist: Gist) -> Gist:
        response = self.github_conn.request(method=HTTPMethod.post,
                                            url=GISTS_ROUTE,
                                            body=gist.to_github())
        return Gist.from_github(response.get('body'))

    def update(self, gist_id: str, gist: Gist) -> Gist:
        response = self.github_conn.request(method=HTTPMethod.put,
                                            url=f'{GISTS_ROUTE}/{gist_id}',
                                            body=gist.to_github())
        return Gist.from_github(response.get('body'))

    def delete(self, gist_id: str) -> dict:
        # TODO: maybe add some implementation
        return self.github_conn.request(method=HTTPMethod.delete,
                                        url=f'{GISTS_ROUTE}/{gist_id}')

    def get_preview_revision(self):
        # TODO!
        return ''

    def star(self, gist_id: str) -> dict:
        return self.github_conn.request(method=HTTPMethod.put,
                                        url=f'{GISTS_ROUTE}/{gist_id}/star',
                                        header={'Content-Length': 0})

    def unstar(self, gist_id: str) -> dict:
        return self.github_conn.request(method=HTTPMethod.delete,
                                        url=f'{GISTS_ROUTE}/{gist_id}/star')

    def is_starred(self, gist_id: str) -> bool:
        response = self.github_conn.request(method=HTTPMethod.get,
                                            url=f'{GISTS_ROUTE}/{gist_id}/star')
        if response.get('status_code') == 204:
            return True
        return False
