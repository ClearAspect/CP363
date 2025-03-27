-- MovieMusicStore Database Selection
use moviemusicstore
;

-- Query 1: Customer Order Summary
-- Returns customer details with their order statistics including:
-- total number of orders, total amount spent, and average order amount
select
    c.customer_id,
    concat(c.first_name, ' ', c.last_name) as customername,
    count(o.order_id) as ordercount,
    sum(o.total_amount) as totalspent,
    avg(o.total_amount) as avgorderamount
from customer c
join `Order` o on c.customer_id = o.customer_id
group by c.customer_id, c.first_name, c.last_name
order by totalspent desc
;

-- Query 2: Movie Actor List
-- Lists all movies with their associated actors concatenated into a single string
select
    m.movie_id,
    m.title,
    group_concat(concat(a.first_name, ' ', a.last_name) separator ', ') as actors
from movie m
join movie_actor ma on m.movie_id = ma.movie_id
join actor a on ma.actor_id = a.actor_id
group by m.movie_id, m.title
order by m.title
;

-- Query 3: High-Value Customers
-- Identifies customers who have spent more than the average order amount
select
    c.customer_id,
    concat(c.first_name, ' ', c.last_name) as customername,
    sum(o.total_amount) as totalspent
from customer c
join `Order` o on c.customer_id = o.customer_id
group by c.customer_id, c.first_name, c.last_name
having sum(o.total_amount) > (select avg(total_amount) from `Order`)
order by totalspent desc
;


-- Query 4: Combined Movie and Album Catalog
-- Combines movies and music albums into a single sorted list
select movie_id as id, title, 'Movie' as type
from movie
union
select album_id as id, title, 'Album' as type
from musicalbum
order by title
;

-- Query 5: Date Range Generation
-- Generates a series of dates from May 1st to May 10th, 2023
with recursive
    daterange as (
        select date('2023-05-01') as report_date
        union all
        select date_add(report_date, interval 1 day)
        from daterange
        where report_date < '2023-05-10'
    )
select *
from daterange
;


-- Query 6: Actors in Multiple Movies
-- Lists actors who have appeared in more than one movie
select
    a.actor_id,
    concat(a.first_name, ' ', a.last_name) as actorname,
    count(ma.movie_id) as moviecount
from actor a
join movie_actor ma on a.actor_id = ma.actor_id
group by a.actor_id, a.first_name, a.last_name
having count(ma.movie_id) > 1
order by moviecount desc
;


-- Query 7: Above Average Customer Orders
-- Identifies orders that exceed the customer's average order amount
select
    o.order_id,
    o.customer_id,
    o.total_amount,
    (
        select avg(o2.total_amount) from `Order` o2 where o2.customer_id = o.customer_id
    ) as customeravgorder
from `Order` o
where
    o.total_amount
    > (select avg(o3.total_amount) from `Order` o3 where o3.customer_id = o.customer_id)
order by o.total_amount desc
;

-- Query 8: Execution Plan Analysis
-- Analyzes the execution plan for the movie-actor query
explain
select
    m.movie_id,
    m.title,
    group_concat(concat(a.first_name, ' ', a.last_name) separator ', ') as actors
from movie m
join movie_actor ma on m.movie_id = ma.movie_id
join actor a on ma.actor_id = a.actor_id
group by m.movie_id, m.title
order by m.title
;


-- Views
CREATE OR REPLACE VIEW CustomerOrderSummaryView AS
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS CustomerName,
    (SELECT COUNT(*) FROM `Order` o WHERE o.customer_id = c.customer_id) AS TotalOrders,
    (SELECT IFNULL(SUM(o.total_amount), 0) FROM `Order` o WHERE o.customer_id = c.customer_id) AS TotalSpent,
    (SELECT IFNULL(AVG(o.total_amount), 0) FROM `Order` o WHERE o.customer_id = c.customer_id) AS AvgOrderAmount
FROM Customer c;


CREATE OR REPLACE VIEW MovieStockDerivedView AS
SELECT 
    m.movie_id,
    m.title,
    m.runtime_minutes,
    DerivedStock.StockRating
FROM Movie m
JOIN (
    SELECT movie_id, (stock_count / 10) AS StockRating
    FROM Movie
) AS DerivedStock ON m.movie_id = DerivedStock.movie_id;


CREATE OR REPLACE VIEW HighValueCustomerOrders AS
SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    o.total_amount
FROM `Order` o
WHERE o.customer_id IN (
    SELECT c.customer_id
    FROM Customer c
    JOIN `Order` o2 ON c.customer_id = o2.customer_id
    GROUP BY c.customer_id
    HAVING SUM(o2.total_amount) > (SELECT AVG(total_amount) FROM `Order`)
)
ORDER BY o.total_amount DESC;


-- View Query Testing Section
-- Test 1: Customer Order Summary View
-- Display all customer order summaries
select *
from customerordersummaryview
;

-- Test 2: Movie Stock Ratings View
-- Display all movie stock ratings
select *
from moviestockderivedview
;

-- Test 3: High Value Customer Orders View
-- Display all high-value customer orders
select *
from highvaluecustomerorders
;

