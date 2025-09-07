# Script used to scrape all categories and all books on the first page in the given link: https://books.toscrape.com/,
# and save the category data and the book data in separate .csv file

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# this function returns the integer value of corrensponding text value of Rating

rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
#Creation of required Dataframe and Variable

df_book_detail = pd.DataFrame(columns=['Name', 'Category', 'Price', 'Stock', 'Rating'])
df_book_detail = df_book_detail.astype({
   'Name': 'string',
   'Category': 'string',
   'Price': 'float64',
   'Stock': 'int64',
  'Rating': 'int64'
  })
df_category = pd.DataFrame(columns=['Category'])
df_category = df_category.astype({'Category': 'string'})
category_list = []  # list to store the categories
idx = 0   # indexing variable

#Extract a beautifulSoup object from the given link

url = "https://books.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

#Extract all the category values and write into the file category.csv

pattern_category = r'catalogue/category/books/[\w-]+_\d+/index\.html'  # sample - catalogue/category/books/travel_2/index.html
for name in soup.find_all("a", href=re.compile(pattern_category)):
    category_list.append(name.text.strip())

df_category = pd.DataFrame({"Category": category_list})
try:
    df_category.to_csv('category.csv', index=False)
except Exception as e:
    print(e)

#Extract all the book details and write into the file book_details.csv

for detail in soup.find_all("article", class_="product_pod"):
    # extract book title
    book_name = detail.find("h3").find("a")["title"]

    # extract the price
    Price = detail.find("p", class_="price_color").text  # extract the price with the pound sign
    match1 = re.search(r'\d*\.?\d+$', Price)  # extract the decimal value of the price
    book_price = float(match1.group(0))

    # extract the rating
    book_rating = rating_map.get(detail.find('p', class_='star-rating')['class'][1])

    # extract the category
    page1 = requests.get(url + detail.find("a").get('href'))  # extract the book link soup
    soup1 = BeautifulSoup(page1.content, "html.parser")
    pattern_book_details = r'../category/books/[\w-]+_\d+/index\.html'  # sample ../category/books/travel_2/index.html
    a_tags = soup1.find('a', href=re.compile(pattern_book_details))
    book_category = a_tags.text

    # extract the stock
    stock_availability = soup1.find('p', class_='instock availability').text.strip()
    match = re.search(r'\((\d+)\s+available\)', stock_availability)
    book_stock = match.group(1)
    df_book_detail.loc[idx] = [book_name, book_category, book_price, book_stock, book_rating]
    idx += 1

# write the extracted book details data into the csv file
try:
    df_book_detail.to_csv('book_details.csv', index=False)
except Exception as e:
    print(e)