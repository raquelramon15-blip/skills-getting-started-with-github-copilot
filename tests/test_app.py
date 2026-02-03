import os
import sys
import copy

# Ensure src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient

import app as app_module
from app import app, activities

client = TestClient(app)


orig_activities = copy.deepcopy(activities)


def setup_function():
    # start each test with a fresh copy
    activities.clear()
    activities.update(copy.deepcopy(orig_activities))


def teardown_function():
    activities.clear()
    activities.update(copy.deepcopy(orig_activities))


def test_get_activities_returns_data():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant_and_reflects_in_get():
    email = "tester@example.com"
    activity = "Chess Club"

    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    assert email in resp2.json()[activity]["participants"]


def test_remove_participant_endpoint():
    email = "removeme@example.com"
    activity = "Tennis Club"

    # Add participant first
    activities[activity]["participants"].append(email)
    assert email in activities[activity]["participants"]

    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]
