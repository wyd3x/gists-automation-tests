import pytest

from infra.github_api.github_rest_client import GitHubAPIClient
from infra.models.gist import Gist
from tests.conftest import generate_files
from utils.deployment_helper import DeploymentHelper

MAX_GENERATED_FILES = 100
PUBLIC_GISTS = 1
PRIVATE_GISTS = 1


class TestGetUsers:
    def test_valid_get_project_as_owner(self,
                                        github_api: GitHubAPIClient,
                                        existing_gist: Gist):
        github_gists = github_api.users.get_gists('wyd3x')

        # Right now this 'hard coded' number based on my acc(wyd3x) ~ have 2 before all(1 private, 1 public)
        # If I had access to DB so I could query the db to get exactly how much gists I`ve
        assert len(github_gists) == PUBLIC_GISTS + PRIVATE_GISTS + 1
        assert github_gists[0] == existing_gist

    def test_valid_get_project_as_guest(self,
                                        github_api: GitHubAPIClient,
                                        non_existing_gist: Gist):
        gist = github_api.gists.create(non_existing_gist)
        non_existing_gist.id = gist.id  # for cleanup

        github_api.remove_auth()
        github_gists = github_api.users.get_gists('wyd3x')

        # github_api.set_auth()
        # Right now this 'hard coded' number based on my acc(wyd3x) ~ have 2 before all(1 private, 1 public)
        # If I had access to DB so I could query the db to get exactly how much gists I`ve
        pub_gists = PUBLIC_GISTS
        pub_gists += 1

        assert pub_gists == len(github_gists)
        assert github_gists[0] == gist

    def test_valid_get_max_per_page_as_owner(self,
                                             github_api: GitHubAPIClient,
                                             non_existing_gist: Gist,
                                             deployment_helper: DeploymentHelper):
        files = generate_files(MAX_GENERATED_FILES)
        non_existing_gist.files = files
        created_gist = deployment_helper.create_gist(non_existing_gist)
        non_existing_gist.id = created_gist.id

        github_gists = github_api.users.get_gists('wyd3x')

        assert len(github_gists) == 3
        assert len(created_gist.files) == len(github_gists[0].files)
        assert github_gists[0] == created_gist

    def test_valid_get_max_per_page_as_guest(self,
                                             github_api: GitHubAPIClient,
                                             non_existing_gist: Gist,
                                             deployment_helper: DeploymentHelper):
        files = generate_files(MAX_GENERATED_FILES)
        non_existing_gist.files = files
        created_gist = deployment_helper.create_gist(non_existing_gist)
        non_existing_gist.id = created_gist.id

        github_api.remove_auth()
        github_gists = github_api.users.get_gists('wyd3x')
        # github_api.set_auth()

        assert len(github_gists) == 2
        assert len(created_gist.files) == len(github_gists[0].files)
        assert github_gists[0] == created_gist

    def test_invalid_get_not_exist_user(self,
                                        github_api: GitHubAPIClient):
        with pytest.raises(Exception):
            github_api.users.get_gists('justRandomNotExistsName')
