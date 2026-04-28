import unittest
from unittest.mock import patch

from gui import sale
from tests._fakes import FakeEntry, FakeLabel, FakeTreeTable


class TestGuiSale(unittest.TestCase):
    @patch("gui.sale.sale_service.calculate_total", return_value={"ok": True, "result": 99})
    def test_handle_calculate_total_success(self, _mock_calc):
        label = FakeLabel()
        product_entry = FakeEntry("apple")
        qty_entry = FakeEntry("2")

        sale.handle_calculate_total(label, product_entry, qty_entry)

        self.assertEqual(label.props["text"], "99")

    @patch("gui.sale.messagebox.showwarning")
    @patch("gui.sale.sale_service.calculate_total", return_value={"ok": False, "message": "bad"})
    def test_handle_calculate_total_failure(self, _mock_calc, mock_warning):
        label = FakeLabel()
        product_entry = FakeEntry("apple")
        qty_entry = FakeEntry("x")

        sale.handle_calculate_total(label, product_entry, qty_entry)

        mock_warning.assert_called_once()

    @patch("gui.sale.update_sale_table")
    @patch("gui.sale.clear_sale_fields")
    @patch("gui.sale.messagebox.showinfo")
    @patch("gui.sale.sale_service.sell_stock", return_value={"ok": True, "message": "done"})
    def test_handle_sell_stock_success(self, _mock_sell, mock_info, mock_clear, mock_update):
        table = FakeTreeTable()
        product_entry = FakeEntry("apple")
        qty_entry = FakeEntry("2")

        sale.handle_sell_stock(table, product_entry, qty_entry)

        mock_info.assert_called_once()
        mock_clear.assert_called_once_with(product_entry, qty_entry)
        mock_update.assert_called_once_with(table)

    @patch("gui.sale.update_sale_table")
    @patch("gui.sale.messagebox.showwarning")
    @patch("gui.sale.sale_service.sell_stock", return_value={"ok": False, "message": "failed"})
    def test_handle_sell_stock_failure(self, _mock_sell, mock_warning, mock_update):
        table = FakeTreeTable()
        product_entry = FakeEntry("apple")
        qty_entry = FakeEntry("200")

        sale.handle_sell_stock(table, product_entry, qty_entry)

        mock_warning.assert_called_once()
        mock_update.assert_called_once_with(table)


if __name__ == "__main__":
    unittest.main()
