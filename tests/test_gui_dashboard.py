import unittest
from unittest.mock import patch

from gui import dashboard
from tests._fakes import FakeTreeTable


class TestGuiDashboard(unittest.TestCase):
    @patch("gui.dashboard.messagebox.showwarning")
    @patch("gui.dashboard.dashboard_service.fetch_number_of_products")
    def test_show_total_products_db_failed(self, mock_fetch, mock_warning):
        mock_fetch.return_value = {"ok": False, "code": "DB_FAILED", "message": "db"}

        result = dashboard.show_total_products()

        self.assertIsNone(result)
        mock_warning.assert_called_once()

    @patch("gui.dashboard.dashboard_service.fetch_recent_sales")
    def test_update_recent_sales_table_success(self, mock_recent_sales):
        table = FakeTreeTable()
        table.insert("", "end", values=("old",))
        mock_recent_sales.return_value = {"ok": True, "result": [("2026-01-01", "apple", 2, 20)]}

        dashboard.update_recent_sales_table(table)

        self.assertEqual(len(table.rows), 1)
        self.assertIn(("2026-01-01", "apple", 2, 20), table.rows.values())

    @patch("gui.dashboard.messagebox.showwarning")
    @patch("gui.dashboard.dashboard_service.fetch_recent_sales")
    def test_update_recent_sales_table_db_failed(self, mock_recent_sales, mock_warning):
        table = FakeTreeTable()
        mock_recent_sales.return_value = {"ok": False, "code": "DB_FAILED", "message": "db"}

        dashboard.update_recent_sales_table(table)

        mock_warning.assert_called_once()


if __name__ == "__main__":
    unittest.main()
