from infra.github_api.github_rest_client import GitHubAPIClient
from infra.models.gist import Gist


class DeploymentHelper:
    def __init__(self,
                 github_api: GitHubAPIClient,):
        self.github_api = github_api

    def create_gist(self,
                    gist: Gist, ) -> Gist:
        return self.github_api.gists.create(gist)

    def delete_gist(self,
                    gist: Gist, ):
        try:
            self.github_api.gists.delete(gist.id)
        except Exception:
            pass
