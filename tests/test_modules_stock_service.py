import unittest
from unittest.mock import MagicMock, patch

from modules import stock_service
from tests._fakes import FakeEntry


class TestStockService(unittest.TestCase):
    @patch("modules.stock_service.config.get_db_connection")
    @patch("modules.stock_service.queries.insert_movement")
    @patch("modules.stock_service.queries.increase_quantity")
    def test_apply_stock_change_in(self, mock_increase, mock_insert, mock_conn):
        cursor = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn

        result = stock_service.apply_stock_change(1, 5, "IN")

        self.assertTrue(result["ok"])
        mock_insert.assert_called_once_with(cursor, 1, 5, "IN")
        mock_increase.assert_called_once_with(cursor, 5, 1)
        conn.commit.assert_called_once()

    @patch("modules.stock_service.config.get_db_connection")
    @patch("modules.stock_service.queries.insert_movement")
    @patch("modules.stock_service.queries.decrease_quantity")
    def test_apply_stock_change_out(self, mock_decrease, mock_insert, mock_conn):
        cursor = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn

        result = stock_service.apply_stock_change(2, 3, "OUT")

        self.assertTrue(result["ok"])
        mock_insert.assert_called_once_with(cursor, 2, 3, "OUT")
        mock_decrease.assert_called_once_with(cursor, 3, 2)

    @patch("modules.stock_service.handle_fetch_products")
    def test_fetch_products_with_stock_levels(self, mock_fetch):
        mock_fetch.return_value = [
            (1, "apple", "fruit", 10, 12, None),
            (2, "banana", "fruit", 8, 5, None),
        ]

        result = stock_service.fetch_products_with_stocklvl(threshold=10)

        self.assertEqual(result[0][-1], "HIGH")
        self.assertEqual(result[1][-1], "LOW")

    @patch("modules.stock_service.fetch_productID", return_value=(1,))
    def test_upgrade_stock_invalid_quantity(self, _mock_id):
        entries = {"name": FakeEntry("apple"), "stock": FakeEntry("abc")}

        result = stock_service.upgrade_stock(entries)

        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "VALIDATION_ERROR")

    @patch("modules.stock_service.fetch_productID", return_value=None)
    def test_upgrade_stock_missing_product(self, _mock_id):
        entries = {"name": FakeEntry("apple"), "stock": FakeEntry("3")}

        result = stock_service.upgrade_stock(entries)

        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "VALIDATION_ERROR")

    @patch("modules.stock_service.apply_stock_change", return_value={"ok": True, "message": "Stock Updated!"})
    @patch("modules.stock_service.product_service.find_product_by_name", return_value=("record",))
    @patch("modules.stock_service.fetch_productID", return_value=(9,))
    def test_upgrade_stock_success(self, _mock_id, _mock_find, mock_apply):
        entries = {"name": FakeEntry("Apple"), "stock": FakeEntry("5")}

        result = stock_service.upgrade_stock(entries)

        self.assertTrue(result["ok"])
        mock_apply.assert_called_once_with(9, 5, "IN")


if __name__ == "__main__":
    unittest.main()
