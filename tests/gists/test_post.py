import pytest

from infra.github_api.github_rest_client import GitHubAPIClient
from infra.models.gist import Gist

MAX_GENERATED_FILES = 100
PUBLIC_GISTS = 1
PRIVATE_GISTS = 1


# Right now in this class most tests looks like GET because I don't have access to DB so i depends on get results
class TestPostValid:
    def test_valid_post_gist(self,
                             github_api: GitHubAPIClient,
                             existing_gist: Gist):
        github_gists = github_api.users.get_gists('wyd3x')

        assert len(github_gists) == PUBLIC_GISTS + PRIVATE_GISTS + 1
        assert github_gists[0] == existing_gist

    def test_invalid_post_gist_as_guest(self,
                                        github_api: GitHubAPIClient,
                                        non_existing_gist: Gist):
        github_api.remove_auth()
        with pytest.raises(Exception):
            assert github_api.gists.create(non_existing_gist)

    def test_valid_unicode_in_description(self,
                                          github_api: GitHubAPIClient,
                                          non_existing_gist: Gist):
        non_existing_gist.description = "בדיקה"
        gist = github_api.gists.create(non_existing_gist)
        non_existing_gist.id = gist.id

        github_gists = github_api.users.get_gists('wyd3x')

        assert github_gists[0] == gist

    def test_valid_unicode_in_filename(self,
                                       github_api: GitHubAPIClient,
                                       non_existing_gist: Gist):
        non_existing_gist.files[0].filename = "בדיקה"
        gist = github_api.gists.create(non_existing_gist)
        non_existing_gist.id = gist.id

        github_gists = github_api.users.get_gists('wyd3x')

        assert github_gists[0] == gist
