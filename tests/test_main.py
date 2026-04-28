import importlib
import unittest
from unittest.mock import MagicMock, patch


class _FakeWidget:
    def __init__(self, *_args, **_kwargs):
        pass

    def pack(self, *_args, **_kwargs):
        return None

    def config(self, *_args, **_kwargs):
        return None

    def pack_propagate(self, *_args, **_kwargs):
        return None


class TestMain(unittest.TestCase):
    @patch("gui.stock.stock_page")
    @patch("gui.sale.sale_page")
    @patch("gui.report.report_page")
    @patch("gui.product.product_page")
    @patch("gui.dashboard.dashboard_page")
    @patch("tkinter.Button", side_effect=lambda *a, **k: _FakeWidget(*a, **k))
    @patch("tkinter.Frame", side_effect=lambda *a, **k: _FakeWidget(*a, **k))
    @patch("tkinter.Tk")
    def test_main_module_loads_with_mocked_tk(
        self,
        mock_tk,
        _mock_frame,
        _mock_button,
        mock_dashboard,
        _mock_product,
        _mock_report,
        _mock_sale,
        _mock_stock,
    ):
        root = MagicMock()
        mock_tk.return_value = root

        if "main" in importlib.sys.modules:
            del importlib.sys.modules["main"]

        importlib.import_module("main")

        root.geometry.assert_called_once()
        root.title.assert_called_once()
        root.minsize.assert_called_once()
        root.mainloop.assert_called_once()
        mock_dashboard.assert_called_once()


if __name__ == "__main__":
    unittest.main()
