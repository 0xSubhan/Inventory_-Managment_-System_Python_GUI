import unittest

from tests._fakes import FakeWidget, FakeWindow
from utility import clear_window


class TestClearWindow(unittest.TestCase):
    def test_clear_main_destroys_all_widgets(self):
        widgets = [FakeWidget(), FakeWidget(), FakeWidget()]
        window = FakeWindow(widgets)

        clear_window.clear_main(window)

        self.assertTrue(all(widget.destroyed for widget in widgets))


if __name__ == "__main__":
    unittest.main()
