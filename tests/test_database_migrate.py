import unittest
from unittest.mock import MagicMock, patch

from database import migrate


class TestDatabaseMigrate(unittest.TestCase):
    @patch("database.migrate.psycopg2.connect")
    def test_ensure_database_exists_skips_existing_database(self, mock_connect):
        admin_connection = MagicMock()
        admin_cursor = MagicMock()
        admin_cursor.fetchone.return_value = (1,)
        admin_connection.cursor.return_value.__enter__.return_value = admin_cursor
        mock_connect.return_value = admin_connection

        migrate._ensure_database_exists()

        admin_cursor.execute.assert_called_once_with(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (migrate.DB_NAME,),
        )
        self.assertEqual(admin_cursor.execute.call_count, 1)
        admin_connection.close.assert_called_once()

    @patch("database.migrate.psycopg2.connect")
    def test_ensure_database_exists_creates_missing_database(self, mock_connect):
        admin_connection = MagicMock()
        admin_cursor = MagicMock()
        admin_cursor.fetchone.return_value = None
        admin_connection.cursor.return_value.__enter__.return_value = admin_cursor
        mock_connect.return_value = admin_connection

        migrate._ensure_database_exists()

        self.assertEqual(admin_cursor.execute.call_count, 2)
        admin_cursor.execute.assert_any_call(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (migrate.DB_NAME,),
        )
        self.assertTrue(
            any(
                "CREATE DATABASE" in str(call.args[0])
                for call in admin_cursor.execute.call_args_list
            )
        )
        admin_connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
