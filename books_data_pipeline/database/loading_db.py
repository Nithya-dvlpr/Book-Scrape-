# Script to load the data from the .cvs files category.csv and book_details.csv into the database BooksToScrape
# Load category.csv data into the table ProductInfo
# Load book_details.csv data into the table ProductDetails

import sys
import pyodbc
import pandas as pd

#Creation of Dataframe by reading the .csv file
try:
    df_book_details = pd.read_csv(r".\book_details.csv")
except FileNotFoundError:
    print("Error: The file 'book_details.csv' was not found.")
    sys.exit(1)
df_book_details["ProductId"] = None
try:
    df_category = pd.read_csv(r".\category.csv")
except FileNotFoundError:
    print("Error: The file 'category.csv' was not found.")
    sys.exit(1)

#Connect to the BooksToScrape database

server = 'nithyadesktop'
database = 'BooksToScrape'
conn=pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database)
cursor = conn.cursor()

#Load data from category.csv filr into ProductInfo Table

insert_query = f"INSERT INTO ProductInfo (ProductCategory,ProductType) VALUES (?,'Book')"
for index, row in df_category.iterrows():
    cursor.execute(insert_query, row['Category'])

#Load the ProductId in the dataframe df_book_details by accessing the ProductInfo table
    # Note: ProductId gets auto-generated while inserting data into ProductInfo table
#ProductId is used as foreign-key to link the data in ProductInfo and ProductDetail tables

cursor.execute("SELECT ProductTypeId,ProductCategory FROM  ProductInfo")
data=cursor.fetchall()
for index,row in df_book_details.iterrows():
    for element in data:
        if element[1]==row['Category']:
            df_book_details.loc[index,"ProductId"] = element[0]
            break
            
#Load data into the ProductDetails Table with the ProductID reference

insert_query = f"INSERT INTO ProductDetail (ProductTypeId,ProductName,ProductPrice,ProductStock,ProductRating) VALUES (?,?,?,?,?)"
for index, row in df_book_details.iterrows():
    cursor.execute(insert_query, row['ProductId'],row['Name'],row['Price'],row['Stock'],row['Rating'])

#Close the connection

conn.commit()
cursor.close()
conn.close()