import unittest
from unittest.mock import MagicMock, patch

from gui import product
from tests._fakes import FakeEntry, FakeTreeTable


class TestGuiProduct(unittest.TestCase):
    def test_clear_form_clears_all_entries(self):
        entries = {"name": FakeEntry("apple"), "price": FakeEntry("10")}

        product.clear_form(entries)

        self.assertEqual(entries["name"].get(), "")
        self.assertEqual(entries["price"].get(), "")

    @patch("gui.product.refresh_table")
    @patch("gui.product.clear_form")
    @patch("gui.product.messagebox.showinfo")
    @patch("gui.product.product_service.save_product", return_value={"ok": True, "message": "saved"})
    def test_handle_save_success(self, _mock_save, mock_info, mock_clear, mock_refresh):
        entries = {"name": FakeEntry("apple")}
        table = FakeTreeTable()

        product.handle_save(entries, table)

        mock_info.assert_called_once()
        mock_clear.assert_called_once_with(entries)
        mock_refresh.assert_called_once_with(table)

    @patch("gui.product.clear_search_field")
    @patch("gui.product.show_search_result")
    @patch("gui.product.product_service.search_product", return_value=("row",))
    def test_handle_search_found(self, _mock_search, mock_show, mock_clear):
        entry = FakeEntry("apple")
        table = FakeTreeTable()

        product.handle_search(entry, table)

        mock_show.assert_called_once_with(table, ("row",))
        mock_clear.assert_called_once_with(entry)

    @patch("gui.product.refresh_table")
    @patch("gui.product.messagebox.showwarning")
    @patch("gui.product.product_service.search_product", return_value=None)
    def test_handle_search_not_found(self, _mock_search, mock_warning, mock_refresh):
        entry = FakeEntry("notfound")
        table = FakeTreeTable()

        product.handle_search(entry, table)

        mock_warning.assert_called_once()
        mock_refresh.assert_called_once_with(table)


if __name__ == "__main__":
    unittest.main()
