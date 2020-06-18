import pytest

from infra.github_api.github_rest_client import GitHubAPIClient
from infra.models.gist import Gist
from utils.deployment_helper import DeploymentHelper


class TestDeleteGist:
    def test_valid_delete_gist(self,
                               github_api: GitHubAPIClient,
                               existing_gist: Gist,
                               deployment_helper: DeploymentHelper):
        deployment_helper.delete_gist(existing_gist)

        with pytest.raises(Exception):
            assert github_api.gists.read(existing_gist.id)

    def test_invalid_delete_gist_as_guest(self,
                                          github_api: GitHubAPIClient,
                                          existing_gist: Gist,
                                          deployment_helper: DeploymentHelper):
        github_api.remove_auth()
        with pytest.raises(Exception):
            assert deployment_helper.delete_gist(existing_gist)

    def test_delete_not_exist_gist(self,
                                   existing_gist: Gist,
                                   deployment_helper: DeploymentHelper):
        deployment_helper.delete_gist(existing_gist)

        with pytest.raises(Exception):
            assert deployment_helper.delete_gist(existing_gist)
