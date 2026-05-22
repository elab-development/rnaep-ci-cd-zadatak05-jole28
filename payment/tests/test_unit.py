import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import os

os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_PASSWORD"] = ""

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

with patch("database.redis", MagicMock()):
    from main import Order


def test_order_total_calculation():
    price = 100
    quantity = 2
    fee = 0.2 * price
    total = 1.2 * price * quantity

    assert fee == 20
    assert total == 240


def test_order_status_default_pending():
    order = Order(
        product_id="1",
        price=100,
        fee=20,
        total=120,
        quantity=1,
        status="pending"
    )

    assert order.status == "pending"