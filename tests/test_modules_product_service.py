import unittest
from unittest.mock import MagicMock, patch

from modules import product_service
from tests._fakes import FakeEntry


class TestProductService(unittest.TestCase):
    @patch("modules.product_service.config.get_db_connection", return_value=None)
    def test_find_product_by_name_db_failure(self, _mock_conn):
        self.assertFalse(product_service.find_product_by_name("apple"))

    @patch("modules.product_service.config.get_db_connection")
    @patch("modules.product_service.queries.insert_product")
    def test_add_product_success(self, mock_insert, mock_get_conn):
        cursor = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value = cursor
        mock_get_conn.return_value = conn

        result = product_service.add_product("apple", "fruit", 10.0, 5)

        self.assertTrue(result["ok"])
        mock_insert.assert_called_once_with(cursor, "apple", "fruit", 10.0, 5)
        conn.commit.assert_called_once()
        cursor.close.assert_called_once()
        conn.close.assert_called_once()

    def test_save_product_empty_field_validation(self):
        entries = {
            "name": FakeEntry(""),
            "category": FakeEntry("fruit"),
            "price": FakeEntry("10"),
            "quantity": FakeEntry("1"),
        }

        result = product_service.save_product(entries)

        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "VALIDATION_ERROR")

    def test_save_product_small_name_validation(self):
        entries = {
            "name": FakeEntry("a"),
            "category": FakeEntry("fruit"),
            "price": FakeEntry("10"),
            "quantity": FakeEntry("1"),
        }

        result = product_service.save_product(entries)

        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "VALIDATION_ERROR")

    def test_save_product_non_numeric_validation(self):
        entries = {
            "name": FakeEntry("apple"),
            "category": FakeEntry("fruit"),
            "price": FakeEntry("abc"),
            "quantity": FakeEntry("x"),
        }

        result = product_service.save_product(entries)

        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "VALIDATION_ERROR")

    @patch("modules.product_service.find_product_by_name", return_value=("exists",))
    def test_save_product_already_exists(self, _mock_find):
        entries = {
            "name": FakeEntry("apple"),
            "category": FakeEntry("fruit"),
            "price": FakeEntry("10"),
            "quantity": FakeEntry("1"),
        }

        result = product_service.save_product(entries)

        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "ALREADY_EXSISTS")

    @patch("modules.product_service.add_product", return_value={"ok": True})
    @patch("modules.product_service.find_product_by_name", return_value=None)
    def test_save_product_success(self, _mock_find, mock_add):
        entries = {
            "name": FakeEntry(" Apple "),
            "category": FakeEntry(" Fruit "),
            "price": FakeEntry("10.5"),
            "quantity": FakeEntry("2"),
        }

        result = product_service.save_product(entries)

        self.assertTrue(result["ok"])
        mock_add.assert_called_once_with("apple", "fruit", 10.5, 2)


if __name__ == "__main__":
    unittest.main()
