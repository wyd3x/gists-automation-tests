import string

import pytest

from infra.github_api.github_rest_client import GitHubAPIClient
from infra.models.gist import Gist
from utils.deployment_helper import DeploymentHelper
from utils.utils import get_random_value


class TestUpdateGist:
    def test_invalid_update_not_exist_gist(self,
                                           github_api: GitHubAPIClient,
                                           existing_gist: Gist,
                                           deployment_helper: DeploymentHelper):
        existing_gist.description = "new testing description"

        deployment_helper.delete_gist(existing_gist)

        with pytest.raises(Exception):
            assert github_api.gists.update(existing_gist.id, existing_gist)

    def test_valid_update_description(self,
                                      github_api: GitHubAPIClient,
                                      existing_gist: Gist):
        existing_gist.description = "new testing description"

        github_api.gists.update(existing_gist.id, existing_gist)

        updated_gist = github_api.gists.read(existing_gist.id)

        assert updated_gist.description == existing_gist.description

    @pytest.mark.parametrize("parameter_name,parameter_value",
                             [("filename", get_random_value(num_chars=10, chars=string.ascii_letters + string.digits,
                                                            postfix=".txt")),
                              ("content", get_random_value(num_chars=100, chars=string.printable))])
    def test_valid_update_file(self,
                               parameter_name: str,
                               parameter_value: str,
                               github_api: GitHubAPIClient,
                               existing_gist: Gist):
        existing_gist.files[0].__setattr__(parameter_name, parameter_value)

        github_api.gists.update(existing_gist.id, existing_gist)

        updated_gist = github_api.gists.read(existing_gist.id)

        assert updated_gist.files[0].__getattribute__(parameter_name) == str(
            existing_gist.files[0].__getattribute__(parameter_name))

    def test_invalid_update_as_guest(self,
                                     github_api: GitHubAPIClient,
                                     existing_gist: Gist):
        existing_gist.description = "new testing description"
        github_api.remove_auth()
        github_api.gists.delete(existing_gist.id)

        with pytest.raises(Exception):
            assert github_api.gists.update(existing_gist.id, existing_gist)
