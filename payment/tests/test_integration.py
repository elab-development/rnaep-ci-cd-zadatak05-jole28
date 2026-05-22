import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import os
from redis_om import NotFoundError

os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_PASSWORD"] = ""

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

mock_redis = MagicMock()

with patch("database.redis", mock_redis):
    from fastapi.testclient import TestClient
    from main import app, Order

client = TestClient(app)


from redis_om import NotFoundError

def test_get_order_not_found():
    with patch.object(Order, "get", side_effect=NotFoundError()):
        response = client.get("/orders/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_app_health_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200