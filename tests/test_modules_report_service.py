import unittest
from unittest.mock import MagicMock, patch

from modules import report_service


class TestReportService(unittest.TestCase):
    def test_validate_date_range_missing_date(self):
        result = report_service.validate_date_range("", "2026-01-01")
        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "VALIDATION_ERROR")

    def test_validate_date_range_invalid_format(self):
        result = report_service.validate_date_range("01-01-2026", "2026-01-01")
        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "VALIDATION_ERROR")

    def test_validate_date_range_from_after_to(self):
        result = report_service.validate_date_range("2026-02-01", "2026-01-01")
        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "VALIDATION_ERROR")

    @patch("modules.report_service.config.get_db_connection")
    @patch("modules.report_service.queries.get_low_stock_products", return_value=[])
    def test_fetch_low_stock_records_no_data(self, _mock_low_stock, mock_conn):
        cursor = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn

        result = report_service.fetch_low_stock_records()

        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "NO_LOW_STOCK")

    def test_fetch_sales_records_by_date_invalid_date_returns_validation(self):
        result = report_service.fetch_sales_records_by_date("2026/01/01", "2026-01-02")
        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "VALIDATION_ERROR")

    @patch("modules.report_service.config.get_db_connection")
    @patch("modules.report_service.queries.get_top_five_products_by_date_range", return_value=[("row",)])
    def test_fetch_top_products_by_date_success(self, _mock_query, mock_conn):
        cursor = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn

        result = report_service.fetch_top_products_by_date("2026-01-01", "2026-01-31", limit=5)

        self.assertTrue(result["ok"])
        self.assertEqual(result["result"], [("row",)])


if __name__ == "__main__":
    unittest.main()
