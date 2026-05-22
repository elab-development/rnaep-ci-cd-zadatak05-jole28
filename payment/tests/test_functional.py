import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import os

os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_PASSWORD"] = ""

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

mock_redis = MagicMock()

with patch("database.redis", mock_redis):
    from fastapi.testclient import TestClient
    from main import app, Order

client = TestClient(app)


def test_create_order_product_not_found():
    mock_response = MagicMock()
    mock_response.status_code = 404

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch("httpx.AsyncClient") as async_client:
        async_client.return_value.__aenter__.return_value = mock_client

        response = client.post("/orders", json={
            "id": "1",
            "quantity": 2
        })

    assert response.status_code == 400
    assert response.json()["detail"] == "Product not found in Inventory"