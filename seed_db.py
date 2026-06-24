import sqlite3
import random
from datetime import datetime, timedelta
 

conn=sqlite3.connect('ecommerce.db')
cursor=conn.cursor()
cursor.executescript("""
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS transactions;
                     

CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        signup_date TEXT,
        country TEXT      
);

CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        price REAL     
);

CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY,
        user_id INTEGER,       
        product_id INTEGER,
        transaction_date TEXT, 
        quantity INTEGER    
);


""")

# INSERT INTO products (product_id, product_name, category, price) VALUES(1, 'Laptop', 'Electronics', 999.99);
# INSERT INTO products (product_id, product_name, category, price) VALUES(2, 'Smartphone', 'Electronics', 499.99);


our_user_data=[]
# Our product catalog: (product_id, name, category, price)
products_to_add = [
    (1, 'Laptop', 'Electronics', 899.99),
    (2, 'Smartphone', 'Electronics', 599.99),
    (3, 'Headphones', 'Electronics', 99.99),
    (4, 'T-Shirt', 'Apparel', 19.99),
    (5, 'Jeans', 'Apparel', 49.99),
    (6, 'Coffee Maker', 'Home', 79.99)
]
our_transaction_data = []

countries = ['USA', 'UK', 'Germany', 'France', 'Australia','India']
for uid in range(1,201):
        country=random.choice(countries)
        signup_date=(datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        our_user_data.append((uid,country,signup_date))
        profile=random.choice(['champion','at-risk','new'])
        
        if profile=='champion':
                num_purchases=random.randint(10,20)
                min_days=0
                max_days=14
                
        elif profile=='at-risk':
                num_purchases=random.randint(1,5)
                min_days=60
                max_days=365

        else:
                num_purchases=random.randint(1,3)
                min_days=0
                max_days=30

        for _ in range(num_purchases):
                product_id=random.choice([1,2,3,4,5,6])
                quantity=random.randint(1,5)
                tx_date=(datetime.now() - timedelta(days=random.randint(min_days,max_days))).strftime('%Y-%m-%d')
                our_transaction_data.append((uid,product_id,tx_date,quantity))


        

cursor.executemany("INSERT INTO users(user_id, country,signup_date) VALUES (?, ?, ?)", our_user_data)
cursor.executemany("INSERT INTO products(product_id, product_name, category, price) VALUES (?, ?, ?, ?)", products_to_add)
cursor.executemany("INSERT INTO transactions(user_id,product_id,transaction_date,quantity) VALUES(?,?,?,?)",our_transaction_data)



conn.commit()
conn.close()


