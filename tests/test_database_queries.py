import unittest
from unittest.mock import MagicMock

from database import queries


class TestDatabaseQueries(unittest.TestCase):
    def test_get_product_by_name_executes_and_fetches(self):
        cursor = MagicMock()
        cursor.fetchone.return_value = ("product",)

        result = queries.get_product_by_name(cursor, "apple")

        self.assertEqual(result, ("product",))
        cursor.execute.assert_called_once()
        self.assertEqual(cursor.execute.call_args.args[1], ("apple",))

    def test_insert_product_executes_insert(self):
        cursor = MagicMock()

        queries.insert_product(cursor, "apple", "fruit", 10.0, 5)

        cursor.execute.assert_called_once()
        self.assertEqual(cursor.execute.call_args.args[1], ("apple", "fruit", 10.0, 5))

    def test_get_all_products_fetches_all(self):
        cursor = MagicMock()
        cursor.fetchall.return_value = [("row",)]

        result = queries.get_all_products(cursor)

        self.assertEqual(result, [("row",)])
        cursor.execute.assert_called_once()
        cursor.fetchall.assert_called_once()

    def test_get_transactions_by_date_range_uses_date_params(self):
        cursor = MagicMock()
        cursor.fetchall.return_value = [("sale",)]

        result = queries.get_transactions_by_date_range(cursor, "2026-01-01", "2026-01-31")

        self.assertEqual(result, [("sale",)])
        self.assertEqual(cursor.execute.call_args.args[1], ("2026-01-01", "2026-01-31"))

    def test_get_top_products_by_date_range_uses_limit(self):
        cursor = MagicMock()
        cursor.fetchall.return_value = [("top",)]

        result = queries.get_top_five_products_by_date_range(cursor, "2026-01-01", "2026-01-31", limit=3)

        self.assertEqual(result, [("top",)])
        self.assertEqual(cursor.execute.call_args.args[1], ("2026-01-01", "2026-01-31", 3))


if __name__ == "__main__":
    unittest.main()
