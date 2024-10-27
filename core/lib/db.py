import sqlite3
from .hash import hash_password

def get_db():
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()

    # Tabel users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(9) CHECK (role IN ('cashier', 'admin', 'superuser')) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Superuser Account
    cursor.execute('''
    INSERT INTO users (username, password, role)
    SELECT ?, ?, ?
    WHERE NOT EXISTS (SELECT 1 FROM users);
    ''', ("superuser", hash_password("superuser"), "superuser"))

    # Tabel products
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        sku VARCHAR(50),
        barcode VARCHAR(50) NOT NULL,
        category_id INTEGER,
        stock INTEGER DEFAULT 0,
        price INTEGER(10) NOT NULL,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );
    ''')

    # Tabel categories
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Tabel stock_movements
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_movements (
        movement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        user_id INTEGER,
        movement_type VARCHAR(3) CHECK (movement_type IN ('in', 'out')) NOT NULL,
        quantity_change INTEGER NOT NULL,
        reason TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ''')

    # Tabel transactions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        customer_id INTEGER,
        paid_amount DECIMAL(10, 2) NOT NULL,
        voucher_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (voucher_id) REFERENCES vouchers(voucher_id)
    );
    ''')

    # Tabel transaction_items
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transaction_items (
        transaction_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        discount DECIMAL(10, 2) DEFAULT 0,
        total DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    ''')

    # Tabel invoices
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoices (
        invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id INTEGER,
        invoice_number VARCHAR(50) NOT NULL UNIQUE,
        issued_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
    );
    ''')

    # Tabel promos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS promos (
        promo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        discount_percentage DECIMAL(5, 2) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    ''')

    # Tabel vouchers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vouchers (
        voucher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        code VARCHAR(50) NOT NULL UNIQUE,
        quota INTEGER,
        discount_value DECIMAL(10, 2) NOT NULL,
        expiration_date DATE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Tabel customers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE,
        phone VARCHAR(20) UNIQUE,
        address TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    conn.commit()
    conn.close()

def init_db():
    try:
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None, None
