import string
from typing import List

import pytest

from infra.github_api.github_rest_client import GitHubAPIClient
from infra.models.file import File
from infra.models.gist import Gist
from tests import config
from utils.deployment_helper import DeploymentHelper
from utils.utils import get_random_value, get_random_from_list


@pytest.fixture(scope="session")
def github_api() -> GitHubAPIClient:
    return GitHubAPIClient(host=config.GITHUB_API,
                           token=config.TOKEN)


@pytest.fixture(autouse=True)
def reset_git_auth(github_api: GitHubAPIClient):
    yield
    github_api.set_auth()


@pytest.fixture(scope="session")
def deployment_helper(github_api: GitHubAPIClient) -> DeploymentHelper:
    return DeploymentHelper(github_api)


def generate_file() -> File:
    return File(content=get_random_value(128, string.printable),
                filename=f'{get_random_value(8, string.ascii_letters)}.txt')


def generate_files(count: int) -> List[File]:
    results = []
    for i in range(count):
        results.append(generate_file())

    return results


def generate_gist(files: List[File] = None) -> Gist:
    if not files:
        files = [generate_file()]

    gist = Gist(description=get_random_value(20, string.printable),
                public=True,
                files=files)

    print(f"Generated data: {gist.__dict__}")

    return gist


@pytest.fixture(scope="function")
def non_existing_gist(deployment_helper: DeploymentHelper, github_api: GitHubAPIClient) -> Gist:
    gist = generate_gist()

    yield gist

    if gist.id is not None:
        github_api.set_auth()
        deployment_helper.delete_gist(gist)


@pytest.fixture(scope="function")
def existing_gist(deployment_helper: DeploymentHelper, github_api: GitHubAPIClient) -> Gist:
    data = generate_gist()
    gist = deployment_helper.create_gist(data)

    print(f"Created Gist: {gist.__dict__}")

    yield gist
    github_api.set_auth()
    deployment_helper.delete_gist(gist)
