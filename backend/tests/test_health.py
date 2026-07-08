from fastapi.testclient import TestClient


def test_health_endpoint_reports_ok(tmp_path, monkeypatch):
    monkeypatch.setenv("ASTRO_LIBRARY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("ASTRO_LIBRARY_LIBRARY_DIR", str(tmp_path / "library"))

    from app.main import app

    with TestClient(app) as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["ok"] is True
