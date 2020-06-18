import copy

import pytest

from infra.github_api.github_rest_client import GitHubAPIClient
from infra.models.gist import Gist


class TestGetRevisionsProject:
    def test_valid_get_revision(self,
                                github_api: GitHubAPIClient,
                                existing_gist: Gist):
        new_local_gist = copy.deepcopy(existing_gist)
        new_local_gist.files[0].content = "new Content"
        github_api.gists.update(existing_gist.id, new_local_gist)

        new_gist = github_api.gists.read(new_local_gist.id)

        assert len(new_gist.history) == 2

        old_gist_by_ref = github_api.gists.read(f'{new_gist.id}/{new_gist.history[1].get("version")}')

        assert old_gist_by_ref.id == new_gist.id
        assert old_gist_by_ref.files[0] != new_gist.files[0]
        assert old_gist_by_ref.files[0].content == existing_gist.files[0].content

    def test_invalid_get_not_exists_revision(self,
                                             github_api: GitHubAPIClient,
                                             existing_gist: Gist):
        new_local_gist = copy.deepcopy(existing_gist)
        new_local_gist.files[0].content = "new Content"
        github_api.gists.update(existing_gist.id, new_local_gist)

        new_gist = github_api.gists.read(new_local_gist.id)

        assert len(new_gist.history) == 2

        with pytest.raises(Exception):
            assert github_api.gists.read(f'{new_gist.id}/{new_gist.history[1].get("version")}asd')
