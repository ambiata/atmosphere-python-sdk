from dataclasses import dataclass
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from atmosphere.custom_activity.server import server

from .activity_for_tests import ExpectedModel


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(server) as c:
        yield c


@dataclass(frozen=True)
class Example:
    a: str
    b: int
    good_prediction: ExpectedModel


@pytest.fixture
def example():
    yield Example(a="abc", b=3, good_prediction=ExpectedModel(a="abc", b=3))
