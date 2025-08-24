import json
from app import app


def test_healthz_ok():
    client = app.test_client()
    res = client.get("/healthz")
    assert res.status_code == 200
    data = json.loads(res.data.decode())
    assert data.get("status") == "ok"


def test_random_endpoint():
    client = app.test_client()
    res = client.get("/api/random?n=2")
    assert res.status_code == 200
    data = json.loads(res.data.decode())
    assert data.get("n") == 2
    assert len(data.get("items", [])) == 2
# Each item must contain required keys
for it in data["items"]:
    for key in ("id", "title", "text"):
        assert key in it
