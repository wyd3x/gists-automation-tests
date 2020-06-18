import pytest

from infra.github_api.github_rest_client import GitHubAPIClient
from infra.models.gist import Gist
from utils.deployment_helper import DeploymentHelper


class TestStarGist:
    def test_valid_star_own_gist(self,
                                 github_api: GitHubAPIClient,
                                 existing_gist: Gist):
        github_api.gists.star(existing_gist.id)

        # Using exists rest api for this check. If I could connect to DB so preferred to check there
        assert github_api.gists.is_starred(existing_gist.id)

    def test_valid_star_other_gist(self,
                                   github_api: GitHubAPIClient):
        github_api.gists.star('ced2366f280feadaea7b')

        # Using exists rest api for this check. If I could connect to DB so preferred to check there
        assert github_api.gists.is_starred('ced2366f280feadaea7b')

    def test_invalid_star_gist_as_guest(self,
                                        github_api: GitHubAPIClient,
                                        existing_gist: Gist):
        github_api.remove_auth()
        with pytest.raises(Exception):
            assert github_api.gists.star(existing_gist.id)

    def test_invalid_star_starred_gist(self,
                                       github_api: GitHubAPIClient,
                                       existing_gist: Gist):
        github_api.gists.star(existing_gist.id)
        with pytest.raises(Exception):
            assert github_api.gists.star(existing_gist.id)

    def test_invalid_star_not_exist_gist(self,
                                         github_api: GitHubAPIClient,
                                         existing_gist: Gist,
                                         deployment_helper: DeploymentHelper):
        deployment_helper.delete_gist(existing_gist)

        with pytest.raises(Exception):
            assert github_api.gists.star(existing_gist.id)
