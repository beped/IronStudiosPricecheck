import requests
import datetime
import sqlite3
from bs4 import BeautifulSoup
from termcolor import colored


# URL to be scraped
url="https://www.ironstudios.com.br/estatua-cyclops-unleashed-deluxe---marvel-comics---art-scale-110---iron-studios-090695/p"
#url = input("Type the url: ")
custom_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
response = requests.get(url, headers=custom_headers)

#Parse the page with beautifulsoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the price tag
price_tag = soup.find('meta', {'data-react-helmet': 'true', 'property': 'product:price:amount'})

# Get the value
product_value = price_tag.get('content', None)

# Find the name tag
product_name_tag = soup.find('span', class_='vtex-store-components-3-x-productBrand')

# Get the value(name) and remove the spaces in the beginning and end of the string with strip()
product_name = product_name_tag.text.strip()

#Get the current time   
current_time = datetime.datetime.now()

# print the value
print(colored("Product: " + product_name + "\nPrice: " + product_value, "yellow"))

# Connect to database, it will create if not exists 
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the tables if not exists
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

# Check if the URL already exists in the products table
cursor.execute('SELECT id FROM products WHERE url = ?', (url,) )
existing_product = cursor.fetchone()

# Insert into products table if the URL does not exist
if existing_product:
    # URL already exists, get the product_id
    print(colored(f"Product: {product_name} is already in the database", "red"))
    product_id = existing_product[0]
else:
    # URL does not exist, insert into products table
    cursor.execute('''
        INSERT INTO products (name, url, creation_datetime) VALUES (?, ?, ?)
    ''', (product_name, url, current_time))

    # Get the last inserted product ID
    product_id = cursor.lastrowid


# Insert into prices table
cursor.execute('''
    INSERT INTO prices (product_id, price, scrape_datetime) VALUES (?, ?, ?)
''', (product_id, product_value, current_time))

conn.commit()

