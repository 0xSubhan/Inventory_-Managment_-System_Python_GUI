import unittest
from unittest.mock import patch

from gui import stock
from tests._fakes import FakeEntry, FakeTreeTable


class TestGuiStock(unittest.TestCase):
    @patch("gui.stock.product.clear_form")
    @patch("gui.stock.refresh_stock_table")
    @patch("gui.stock.messagebox.showinfo")
    @patch("gui.stock.stock_service.upgrade_stock", return_value={"ok": True, "message": "done"})
    def test_handle_stock_upgrade_success(self, _mock_upgrade, mock_info, mock_refresh, mock_clear):
        entries = {"name": FakeEntry("apple"), "stock": FakeEntry("4")}
        table = FakeTreeTable()

        stock.handle_stock_upgrade(entries, table)

        mock_info.assert_called_once()
        mock_refresh.assert_called_once_with(table)
        mock_clear.assert_called_once_with(entries)

    @patch("gui.stock.clear_search_field")
    @patch("gui.stock.show_stock_search_result")
    @patch("gui.stock.stock_service.fetch_product", return_value=(1, "apple", "fruit", 10, 11, None))
    def test_handle_stock_search_found(self, _mock_fetch, mock_show, mock_clear):
        entry = FakeEntry("apple")
        table = FakeTreeTable()

        stock.handle_stock_search(entry, table, threshold=10)

        mock_show.assert_called_once()
        mock_clear.assert_called_once_with(entry)

    @patch("gui.stock.refresh_stock_table")
    @patch("gui.stock.clear_search_field")
    @patch("gui.stock.messagebox.showwarning")
    @patch("gui.stock.stock_service.fetch_product", return_value=None)
    def test_handle_stock_search_not_found(self, _mock_fetch, mock_warning, mock_clear, mock_refresh):
        entry = FakeEntry("missing")
        table = FakeTreeTable()

        stock.handle_stock_search(entry, table)

        mock_warning.assert_called_once()
        mock_clear.assert_called_once_with(entry)
        mock_refresh.assert_called_once_with(table)


if __name__ == "__main__":
    unittest.main()
