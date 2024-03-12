import requests
import datetime
import sqlite3
from bs4 import BeautifulSoup
from termcolor import colored

from scrap_functions import *

# Read the URLs to be scraped
with open('urls.txt', 'r') as file:
    urls = file.read().splitlines()

# Open connection with the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
# Check if the tables already exist in the database, if not create them
check_db(conn, cursor)

for url in urls:
    product_name, product_value, current_time = scrape_product(url)

    save_to_database(conn, cursor, product_name, product_value, url, current_time)

    # print the value
    print((colored("Name: ","yellow"))+product_name) 
    print((colored("Price: ","yellow"))+product_value)
    