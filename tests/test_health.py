from app.main import create_app


def test_health_route():
    app = create_app()
    routes = [r.path for r in app.routes]
    assert "/health" in routes
