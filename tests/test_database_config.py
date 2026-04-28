import unittest
from unittest.mock import MagicMock, patch

from database import config


class TestDatabaseConfig(unittest.TestCase):
    @patch("database.config.psycopg2.connect")
    def test_get_db_connection_success(self, mock_connect):
        fake_connection = MagicMock()
        mock_connect.return_value = fake_connection

        result = config.get_db_connection()

        self.assertIs(result, fake_connection)
        mock_connect.assert_called_once()

    @patch("database.config.psycopg2.connect")
    def test_get_db_connection_failure_returns_none(self, mock_connect):
        mock_connect.side_effect = Exception("connection failed")

        result = config.get_db_connection()

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
