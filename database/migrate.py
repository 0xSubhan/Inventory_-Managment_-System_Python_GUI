"""
PostgreSQL Migration Script for Inventory Management System.

Checks for the existence of required tables (product, sales, stock_movements)
and creates any that are missing, along with their sequences, indexes,
constraints, and foreign keys.

Usage:
    python -m database.migrate          # from project root
    python database/migrate.py          # direct execution
"""

import sys
import os

import psycopg2
from psycopg2 import sql

# ---------------------------------------------------------------------------
# Allow direct execution (python database/migrate.py) by ensuring the
# project root is on sys.path so that `from database.config import ...` works.
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from database.config import get_db_connection
from database.config import DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT

# ── Required tables ────────────────────────────────────────────────────────
REQUIRED_TABLES = ["product", "sales", "stock_movements"]

# ── DDL statements (order matters – parent tables first) ───────────────────

CREATE_PRODUCT = """
CREATE TABLE IF NOT EXISTS product (
    productid   SERIAL          PRIMARY KEY,
    name        VARCHAR(80)     NOT NULL,
    category    VARCHAR(80)     NOT NULL,
    price       NUMERIC(6, 2)   NOT NULL,
    quantity    INTEGER         NOT NULL,
    added_at    TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_SALES = """
CREATE TABLE IF NOT EXISTS sales (
    sale_id     SERIAL          PRIMARY KEY,
    productid   INTEGER         NOT NULL
                    REFERENCES product(productid) ON DELETE CASCADE,
    quantity    INTEGER         NOT NULL
                    CHECK (quantity > 0),
    sale_price  NUMERIC(10, 2)  NOT NULL
                    CHECK (sale_price > 0),
    total_price NUMERIC(10, 2)  NOT NULL
                    CHECK (total_price > 0),
    sale_date   TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_STOCK_MOVEMENTS = """
CREATE TABLE IF NOT EXISTS stock_movements (
    movement_id     SERIAL          PRIMARY KEY,
    product_id      INTEGER
                        REFERENCES product(productid) ON DELETE CASCADE,
    change_quantity  INTEGER         NOT NULL,
    movement_type   VARCHAR(20)
                        CHECK (movement_type IN ('IN', 'OUT')),
    reference        VARCHAR(50),
    movement_date    TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);
"""

# Ordered so that parent tables are created before children.
TABLE_DDL = {
    "product":         CREATE_PRODUCT,
    "sales":           CREATE_SALES,
    "stock_movements": CREATE_STOCK_MOVEMENTS,
}


def _ensure_database_exists():
    """Create the target database if it does not already exist."""
    if not DB_NAME:
        print("✗ Migration aborted – DB_NAME is not configured.")
        sys.exit(1)

    admin_connection = None

    try:
        admin_connection = psycopg2.connect(
            host=DB_HOST,
            database="postgres",
            port=DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD,
        )
        admin_connection.autocommit = True

        with admin_connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (DB_NAME,),
            )
            if cursor.fetchone():
                print(f"✓ Database '{DB_NAME}' already exists.")
                return

            print(f"⚙ Creating database '{DB_NAME}' …", end=" ")
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME))
            )
            print("done.")

    except Exception as error:
        print(f"✗ Migration aborted – could not create database '{DB_NAME}': {error}")
        sys.exit(1)

    finally:
        if admin_connection is not None:
            admin_connection.close()


def _get_existing_tables(cursor) -> set:
    """Return a set of user-table names that already exist in the public schema."""
    cursor.execute("""
        SELECT tablename
        FROM   pg_catalog.pg_tables
        WHERE  schemaname = 'public';
    """)
    return {row[0] for row in cursor.fetchall()}


def run_migration():
    """Run the migration: create any missing tables."""
    _ensure_database_exists()

    connection = get_db_connection()
    if connection is None:
        print("✗ Migration aborted – could not connect to the database.")
        sys.exit(1)

    try:
        cursor = connection.cursor()
        existing = _get_existing_tables(cursor)

        missing = [t for t in REQUIRED_TABLES if t not in existing]

        if not missing:
            print("✓ All required tables already exist. Nothing to do.")
            for t in REQUIRED_TABLES:
                print(f"    • {t}")
            return

        print(f"⚙ Detected {len(missing)} missing table(s): {', '.join(missing)}")

        for table_name in REQUIRED_TABLES:          # iterate in dependency order
            if table_name in missing:
                print(f"  → Creating table: {table_name} …", end=" ")
                cursor.execute(TABLE_DDL[table_name])
                print("done.")

        connection.commit()
        print("✓ Migration completed successfully.")

        # Verify
        existing_after = _get_existing_tables(cursor)
        still_missing = [t for t in REQUIRED_TABLES if t not in existing_after]
        if still_missing:
            print(f"✗ Warning: the following tables are still missing: {still_missing}")
        else:
            print("✓ Verification passed – all tables present:")
            for t in REQUIRED_TABLES:
                print(f"    • {t}")

    except Exception as e:
        connection.rollback()
        print(f"✗ Migration failed: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    print("━" * 50)
    print("  Inventory System – PostgreSQL Migration")
    print("━" * 50)
    run_migration()
