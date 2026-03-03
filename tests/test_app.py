from src import app as app_module


def test_root_redirect(client):
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 307
    assert resp.headers.get("location", "").endswith("/static/index.html")


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    email = "newstudent@mergington.edu"
    resp = client.post("/activities/Chess Club/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_already_signed_up(client):
    email = "michael@mergington.edu"
    resp = client.post("/activities/Chess Club/signup", params={"email": email})
    assert resp.status_code == 400


def test_signup_activity_not_found(client):
    resp = client.post("/activities/Nonexistent/signup", params={"email": "x@x.com"})
    assert resp.status_code == 404


def test_unregister_success(client):
    email = "michael@mergington.edu"
    resp = client.delete("/activities/Chess Club/signup", params={"email": email})
    assert resp.status_code == 200
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_unregister_not_signed_up(client):
    email = "nobody@mergington.edu"
    resp = client.delete("/activities/Chess Club/signup", params={"email": email})
    assert resp.status_code == 400
