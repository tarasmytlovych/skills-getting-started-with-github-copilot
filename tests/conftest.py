import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture
def client():
    with TestClient(app_module.app) as c:
        yield c


@pytest.fixture(autouse=True)
def restore_activities():
    """Deep-copy the in-memory `activities` state and restore after each test."""
    original = copy.deepcopy(getattr(app_module, "activities", {}))
    yield
    app_module.activities = original
