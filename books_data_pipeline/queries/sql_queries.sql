--SQL script for the queries

use BooksToScrape;

-- the top three categories with the highest average rating and the lower price

select top 5 ProductInfo.ProductCategory,avg(ProductDetail.ProductPrice) as AveragePrice,avg(ProductDetail.ProductRating) as AverageRating 
	from ProductInfo 
	join ProductDetail 
	on ProductInfo.ProductTypeId = ProductDetail.ProductTypeId
  group by ProductInfo.ProductCategory order by avg(ProductDetail.ProductRating) desc,avg(ProductDetail.ProductPrice);

--the top 5 books by rating
select top 5 ProductName,ProductRating,ProductPrice from ProductDetail order by ProductRating desc, ProductName asc; 
