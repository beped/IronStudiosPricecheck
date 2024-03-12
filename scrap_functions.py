# scraping_functions.py

import requests
from bs4 import BeautifulSoup
from termcolor import colored
import sqlite3
import datetime

#Function to scrape the product and save product name, price and current time
def scrape_product(url):
    custom_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=custom_headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Get the Name
    product_name_tag = soup.find('span', class_='vtex-store-components-3-x-productBrand')
    product_name = product_name_tag.text.strip()
    # Get the price
    price_tag = soup.find('meta', {'data-react-helmet': 'true', 'property': 'product:price:amount'})
    if price_tag:
        product_value = price_tag.get('content', None)
    else:
        product_value = "0"
    #Get the current time and date
    current_time = datetime.datetime.now()

    return product_name, product_value, current_time

def check_db(conn, cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            url TEXT,
            creation_datetime TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            scrape_datetime TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    conn.commit()

#Function to save the product in the database
def save_to_database(conn, cursor, product_name, product_value, url, current_time):
    cursor.execute('SELECT id FROM products WHERE url = ?', (url,) )
    existing_product = cursor.fetchone()

    if existing_product:
        print(colored(f"Product: {product_name} is already in the database", "red"))
        product_id = existing_product[0]
    else:
        cursor.execute('''
            INSERT INTO products (name, url, creation_datetime) VALUES (?, ?, ?)
        ''', (product_name, url, current_time))

        product_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO prices (product_id, price, scrape_datetime) VALUES (?, ?, ?)
    ''', (product_id, product_value, current_time))

    conn.commit()
