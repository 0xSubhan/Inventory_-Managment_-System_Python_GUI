import unittest
from unittest.mock import patch

from gui import report
from tests._fakes import FakeButton, FakeEntry, FakeTreeTable


class TestGuiReport(unittest.TestCase):
    def test_get_date_value_returns_empty_for_placeholder(self):
        entry = FakeEntry(report.DATE_PLACEHOLDER)
        self.assertEqual(report.get_date_value(entry), "")

    def test_reset_date_entry_sets_placeholder(self):
        entry = FakeEntry("2026-01-01")

        report.reset_date_entry(entry)

        self.assertEqual(entry.get(), report.DATE_PLACEHOLDER)
        self.assertEqual(entry.fg, "gray")

    @patch("gui.report.insert_table_rows")
    @patch("gui.report.empty_report_table")
    @patch("gui.report.report_service.fetch_sales_records_by_date")
    def test_handle_filter_report_sales_success(self, mock_fetch, mock_empty, mock_insert):
        result_table = FakeTreeTable()
        from_entry = FakeEntry("2026-01-01")
        to_entry = FakeEntry("2026-01-31")
        mock_fetch.return_value = {"ok": True, "result": [("row",)]}
        report.selected_report_type = "sales"

        report.handle_filter_report(result_table, from_entry, to_entry)

        mock_empty.assert_called_once_with(result_table)
        mock_insert.assert_called_once_with(result_table, [("row",)])

    @patch("gui.report.messagebox.showwarning")
    def test_handle_filter_report_lowstock_warns(self, mock_warning):
        result_table = FakeTreeTable()
        from_entry = FakeEntry("2026-01-01")
        to_entry = FakeEntry("2026-01-31")
        report.selected_report_type = "lowstock"

        report.handle_filter_report(result_table, from_entry, to_entry)

        mock_warning.assert_called_once()

    @patch("gui.report.insert_table_rows")
    @patch("gui.report.sale_service.fetch_all_transactions", return_value={"ok": True, "result": [("sale",)]})
    def test_handle_sales_report_updates_button_and_table(self, _mock_sales, mock_insert):
        table = FakeTreeTable()
        sale_btn = FakeButton()
        low_btn = FakeButton()
        top_btn = FakeButton()
        buttons = (sale_btn, low_btn, top_btn)

        report.handle_sales_report(table, sale_btn, buttons)

        self.assertEqual(report.selected_report_type, "sales")
        self.assertEqual(sale_btn.state, "disabled")
        mock_insert.assert_called_once_with(table, [("sale",)])

    @patch("gui.report.handle_lowstock_report")
    def test_handle_clear_filter_routes_to_selected_report(self, mock_lowstock):
        result_table = FakeTreeTable()
        from_entry = FakeEntry("2026-01-01")
        to_entry = FakeEntry("2026-01-31")
        sale_btn = FakeButton()
        low_btn = FakeButton()
        top_btn = FakeButton()
        buttons = (sale_btn, low_btn, top_btn)
        report.selected_report_type = "lowstock"

        report.handle_clear_filter(result_table, from_entry, to_entry, sale_btn, low_btn, top_btn, buttons)

        mock_lowstock.assert_called_once_with(result_table, low_btn, buttons)
        self.assertEqual(from_entry.get(), report.DATE_PLACEHOLDER)
        self.assertEqual(to_entry.get(), report.DATE_PLACEHOLDER)


if __name__ == "__main__":
    unittest.main()
