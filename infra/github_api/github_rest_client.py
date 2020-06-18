import requests
from retrying import retry

from infra.github_api.consts.http_method import HTTPMethod
from infra.github_api.handlers.gists_handler import GistsHandler
from infra.github_api.handlers.users_handler import UsersHandler


# Connection Errors can cause because temporary connection failure or OpenShift
def retry_if_connection_error(exception: Exception):
    return isinstance(exception, requests.exceptions.ConnectionError) or \
           str(exception).__contains__("ProtocolError")


class GitHubAPIClient:
    def __init__(self,
                 host: str,
                 token: str = None):
        self._session = requests.Session()
        self.token = token
        self._update_header('Accept', 'application/vnd.github.v3+json')

        self.base_url = host
        self.users = UsersHandler(self)
        self.gists = GistsHandler(self)

        self.set_auth()

    def set_auth(self):
        if self.token:
            self._update_header('Authorization', f'token {self.token}')

    def remove_auth(self):
        self._session.headers.pop('Authorization')

    def _update_header(self, key, value):
        self._session.headers.update({key: value})

    @retry(retry_on_exception=retry_if_connection_error, stop_max_attempt_number=2, wait_fixed=2000)
    def request(self,
                method: HTTPMethod,
                url: str,
                body: dict = None,
                headers: dict = None):
        if headers is None:
            headers = {}

        url = self.base_url + url

        response = self._session.request(method=method.name, url=url, json=body, headers=headers)

        body = None
        try:
            body = response.json()
        except Exception:
            body = response.text

        result = {
            'body': body,
            'status_code': response.status_code
        }

        return result
