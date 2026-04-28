import unittest
from unittest.mock import MagicMock, patch

from modules import sale_service


class TestSaleService(unittest.TestCase):
    @patch("modules.sale_service.config.get_db_connection")
    @patch("modules.sale_service.queries.get_product_by_name", return_value=("record",))
    def test_calculate_total_invalid_quantity(self, _mock_product, mock_conn):
        cursor = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn

        result = sale_service.calculate_total("apple", "x")

        self.assertFalse(result["ok"])
        self.assertIn("Number", result["message"])

    @patch("modules.sale_service.config.get_db_connection")
    @patch("modules.sale_service.queries.get_product_price", return_value=(20,))
    @patch("modules.sale_service.queries.get_product_by_name", return_value=("record",))
    def test_calculate_total_success(self, _mock_product, _mock_price, mock_conn):
        cursor = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn

        result = sale_service.calculate_total("apple", "3")

        self.assertTrue(result["ok"])
        self.assertEqual(result["result"], 60)

    @patch("modules.sale_service.handle_fetch_transactions", return_value=[])
    def test_fetch_all_transactions_no_record(self, _mock_fetch):
        result = sale_service.fetch_all_transactions()
        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "NO_RECORD")

    @patch("modules.sale_service.config.get_db_connection")
    @patch("modules.sale_service.queries.get_product_quantity", return_value=(2,))
    @patch("modules.sale_service.queries.get_productID_by_productName", return_value=(10,))
    @patch("modules.sale_service.queries.get_product_price", return_value=(20,))
    @patch("modules.sale_service.queries.get_product_by_name", return_value=("record",))
    def test_sell_stock_not_enough_stock(
        self,
        _mock_product,
        _mock_price,
        _mock_product_id,
        _mock_quantity,
        mock_conn,
    ):
        cursor = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn

        result = sale_service.sell_stock("apple", "3")

        self.assertFalse(result["ok"])
        self.assertIn("Not Enough Stock", result["message"])

    @patch("modules.sale_service.config.get_db_connection")
    @patch("modules.sale_service.queries.insert_sale_transaction")
    @patch("modules.sale_service.stock_service.apply_stock_change")
    @patch("modules.sale_service.queries.get_product_quantity", return_value=(10,))
    @patch("modules.sale_service.queries.get_productID_by_productName", return_value=(7,))
    @patch("modules.sale_service.queries.get_product_price", return_value=(30,))
    @patch("modules.sale_service.queries.get_product_by_name", return_value=("record",))
    def test_sell_stock_success(
        self,
        _mock_product,
        _mock_price,
        _mock_product_id,
        _mock_quantity,
        mock_apply,
        mock_insert_sale,
        mock_conn,
    ):
        cursor = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn

        result = sale_service.sell_stock("apple", "2")

        self.assertTrue(result["ok"])
        mock_apply.assert_called_once_with((7,), 2, "OUT")
        mock_insert_sale.assert_called_once_with(cursor, (7,), 2, 30, 60)
        conn.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
