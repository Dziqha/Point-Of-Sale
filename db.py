# db.py
import sqlite3

def init_db():
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        price REAL,
                        stock INTEGER,
                        description TEXT,
                        category TEXT,
                        discount REAL DEFAULT 0)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        total REAL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS transaction_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        transaction_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        FOREIGN KEY(transaction_id) REFERENCES transactions(id),
                        FOREIGN KEY(product_id) REFERENCES products(id))''')
    
    conn.commit()
    conn.close()

def add_product(name, price, stock, description, category):
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, price, stock, description, category) VALUES (?, ?, ?, ?, ?)
    ''', (name, price, stock, description, category))
    
    conn.commit()
    print("Product added:", name, price, stock, description, category)  # Debugging
    conn.close()

def get_products():
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products
