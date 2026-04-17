# Inventory Management System (Python GUI + PostgreSQL)

A desktop Inventory Management System built with **Python Tkinter** and **PostgreSQL**.  
It helps you manage products, stock, sales, and reports in a single GUI app.

**Owner:** [0xSubhan](https://github.com/0xSubhan)

## What this project does

This application provides:

1. **Dashboard** with key business metrics:
   - total products
   - total stock
   - low-stock count
   - total revenue
   - recent sales table
2. **Product Management**:
   - add products
   - search products by name
   - view product list
3. **Stock Management**:
   - restock existing products
   - view current stock level (HIGH/LOW)
4. **Sales Management**:
   - calculate sale total before checkout
   - sell products and record transactions
   - view sales history
5. **Reports**:
   - sales report
   - low stock report
   - top 5 products report
   - date-range filtering for Sales and Top Products (`YYYY-MM-DD`)
   - clear filter button to reset entries and report data

## Tech stack

- **Language:** Python
- **GUI:** Tkinter (`tkinter`, `ttk`)
- **Database:** PostgreSQL
- **DB Driver:** `psycopg2`
- **Environment config:** `python-dotenv`

## Project structure

```text
.
├── main.py                   # App entry point and sidebar navigation
├── gui/                      # Tkinter pages (dashboard, product, stock, sale, report)
├── modules/                  # Business/service layer
├── database/
│   ├── config.py             # PostgreSQL connection via .env
│   └── queries.py            # Central SQL query functions
└── utility/
    └── clear_window.py       # Reusable UI clear helper
```

## How to run

### 1. Prerequisites

- Python 3.10+ (3.12 recommended)
- PostgreSQL running locally or reachable from your machine

### 2. Install dependencies

From project root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install psycopg2-binary python-dotenv
```

### 3. Configure database environment

Create `database/.env`:

```env
DB_NAME=your_database_name
DB_HOST=127.0.0.1
DB_USERNAME=your_postgres_user
DB_PASSWORD=your_password
DB_PORT=5432
```

### 4. Create required tables

Run these SQL statements in your PostgreSQL database:

```sql
CREATE TABLE IF NOT EXISTS product (
    productid SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    quantity INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS stock_movements (
    movement_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES product(productid),
    change_quantity INTEGER NOT NULL,
    movement_type VARCHAR(10),
    reference VARCHAR(255),
    movement_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id SERIAL PRIMARY KEY,
    productid INTEGER NOT NULL REFERENCES product(productid),
    quantity INTEGER NOT NULL,
    sale_price NUMERIC(12,2) NOT NULL,
    total_price NUMERIC(12,2) NOT NULL,
    sale_date TIMESTAMP DEFAULT NOW()
);
```

### 5. Start the application

```bash
python main.py
```

## How to use the app

### Dashboard
- Open app → Dashboard loads by default.
- Use it for quick status and recent activity.

### Products
- Add product details and click **Save**.
- Use **Search** to find a product by name.
- Use **Refresh Table** to reload all products.

### Stocks
- Enter product name + quantity and click **Restock**.
- Stock table shows stock level status.

### Sales
- Enter product name and quantity.
- Click **Calculate Total** to preview total.
- Click **SELL BUTTON** to complete sale and record transaction.

### Reports
- **Sales Report:** full transaction list.
- **Low Stock:** products below low-stock threshold.
- **Top Products:** ranked top 5 by units sold/revenue.
- Date filter:
  - set **From Date** and **To Date** in `YYYY-MM-DD`
  - click **Filter**
  - click **Clear** to reset filter + entries

## Technical architecture (high-level) (3-Tier Architecture)

1. **GUI layer (`gui/`)**
   - Handles user actions and rendering.
2. **Service layer (`modules/`)**
   - Validates input and coordinates workflow.
3. **Data layer (`database/queries.py`)**
   - Encapsulates raw SQL queries.
4. **Connection layer (`database/config.py`)**
   - Creates PostgreSQL connections from environment variables.

This layered approach keeps SQL centralized and UI logic cleaner.

## Notes

- Product name matching is mostly handled in lowercase in service/UI logic.
- The report date format is strict: `YYYY-MM-DD`.
- If DB credentials are wrong or PostgreSQL is unavailable, the app will show warning/error messages in UI.
