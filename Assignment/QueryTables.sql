use moviemusicstore
;

-- Query 1: List all customers with their orders (using JOIN)
select
    c.customer_id,
    concat(c.first_name, ' ', c.last_name) as customername,
    o.order_id,
    o.order_date,
    o.total_amount
from customer c
join `Order` o on c.customer_id = o.customer_id
order by c.customer_id, o.order_date
;

-- Query 2: Subquery to find movies with runtime greater than the average runtime
select movie_id, title, runtime_minutes
from movie
where runtime_minutes > (select avg(runtime_minutes) from movie)
;

-- Query 3: Subquery to list customers who have placed orders
select customer_id, first_name, last_name
from customer
where customer_id in (select distinct customer_id from `Order`)
;

-- Query 4: Correlated subquery: Find orders whose total amount is greater than 
-- the average order amount for that customer
select o.order_id, o.customer_id, o.total_amount
from `Order` o
where
    o.total_amount
    > (select avg(o2.total_amount) from `Order` o2 where o2.customer_id = o.customer_id)
;

-- Query 5: Window function: Rank movies by stock_count
select
    movie_id, title, stock_count, rank() over (order by stock_count desc) as stockrank
from movie
;

-- Query 6: Window function: List orders with row number partitioned by customer
select
    order_id,
    customer_id,
    total_amount,
    row_number() over (partition by customer_id order by order_date) as orderrank
from `Order`
order by customer_id, order_date
;

-- Query 7: Window function: Divide orders into 3 groups based on total_amount using
-- NTILE
select
    order_id,
    customer_id,
    total_amount,
    ntile(3) over (order by total_amount desc) as amountgroup
from `Order`
order by total_amount desc
;

-- Query 8: Aggregation: Count number of orders per customer and sum total spent
select customer_id, count(order_id) as ordercount, sum(total_amount) as totalspent
from `Order`
group by customer_id
order by ordercount desc
;

-- Query 9: Subquery: List customers who have not placed any orders
select customer_id, first_name, last_name
from customer
where customer_id not in (select customer_id from `Order`)
;

-- Query 10: Correlated subquery: List actors who have acted in more than 1 movie
select
    a.actor_id,
    concat(a.first_name, ' ', a.last_name) as actorname,
    (select count(*) from movie_actor ma where ma.actor_id = a.actor_id) as moviecount
from actor a
where (select count(*) from movie_actor ma where ma.actor_id = a.actor_id) > 1
;

-- View 1: Customer Order Summary View with calculated fields (total orders and total
-- spent)
CREATE OR REPLACE VIEW CustomerOrderSummary AS
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS CustomerName,
    COUNT(o.order_id) AS TotalOrders,
    IFNULL(SUM(o.total_amount), 0) AS TotalSpent
FROM Customer c
LEFT JOIN `Order` o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY TotalSpent DESC;


-- View 2: Movie Stock Ranking View with window function (ranking movies by stock)
CREATE OR REPLACE VIEW MovieStockRanking AS
SELECT movie_id, title, stock_count,
       RANK() OVER (ORDER BY stock_count DESC) AS StockRank
FROM Movie;


-- View 3: Artist Album Summary View with calculated field (album count per artist)
CREATE OR REPLACE VIEW ArtistAlbumSummary AS
SELECT 
    a.artist_id,
    a.artist_name,
    COUNT(aa.album_id) AS AlbumCount
FROM Artist a
LEFT JOIN Album_Artist aa ON a.artist_id = aa.artist_id
GROUP BY a.artist_id, a.artist_name
ORDER BY AlbumCount DESC;

-- View Customer Order Summary
select *
from customerordersummary
;

-- View Movie Stock Ranking
select *
from moviestockranking
;

-- View Artist Album Summary
select *
from artistalbumsummary
;

