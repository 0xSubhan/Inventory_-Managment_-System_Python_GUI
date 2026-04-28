import unittest
from unittest.mock import MagicMock, patch

from modules import dashboard_service


class TestDashboardService(unittest.TestCase):
    @patch("modules.dashboard_service.config.get_db_connection", return_value=None)
    def test_fetch_number_of_products_db_failed(self, _mock_conn):
        result = dashboard_service.fetch_number_of_products()
        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "DB_FAILED")

    @patch("modules.dashboard_service.config.get_db_connection")
    @patch("modules.dashboard_service.queries.get_number_of_products", return_value=(5,))
    def test_fetch_number_of_products_success(self, _mock_count, mock_conn):
        cursor = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn

        result = dashboard_service.fetch_number_of_products()

        self.assertTrue(result["ok"])
        self.assertEqual(result["result"], 5)

    @patch("modules.dashboard_service.config.get_db_connection")
    @patch("modules.dashboard_service.queries.get_total_stocks", return_value=(None,))
    def test_fetch_total_stocks_no_stocks(self, _mock_stocks, mock_conn):
        cursor = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn

        result = dashboard_service.fetch_total_stocks()

        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "NO_STOCKS")
        self.assertEqual(result["result"], 0)

    @patch("modules.dashboard_service.config.get_db_connection")
    @patch("modules.dashboard_service.queries.get_recent_sales", return_value=[])
    def test_fetch_recent_sales_no_records(self, _mock_sales, mock_conn):
        cursor = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn

        result = dashboard_service.fetch_recent_sales()

        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "NO_SALES_RECORD")


if __name__ == "__main__":
    unittest.main()
