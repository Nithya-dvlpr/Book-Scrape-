-- Setup script for the  database BooksToScrape and tables ProductInfo, ProductDetail

DROP DATABASE IF EXISTS BooksToScrape;
CREATE DATABASE  BooksToScrape; 

USE BooksToScrape;


DROP TABLE IF EXISTS ProductDetail,ProductInfo;

CREATE TABLE ProductInfo (
    ProductTypeId INT IDENTITY(1,1), 
    ProductType VARCHAR(40) NOT NULL,
    ProductCategory VARCHAR(40) NOT NULL,
    PRIMARY KEY (ProductTypeId)
);

CREATE TABLE ProductDetail (
	ProductId		int		IDENTITY(1,1),
    ProductTypeId   int			   NOT NULL,
    ProductName     varCHAR(256)   NOT NULL,
	ProductPrice			float,
	ProductStock			int,
	ProductRating			int,
    PRIMARY KEY (ProductId),
	FOREIGN KEY (ProductTypeId)  REFERENCES ProductInfo (ProductTypeId)   

);
