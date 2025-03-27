use MovieMusicStore;

-- Insert Customers
INSERT INTO Customer (first_name, last_name, phone, email, join_date, status)
VALUES 
('John', 'Doe', '1234567890', 'john.doe@example.com', '2023-01-15', 'ACTIVE'),
('Jane', 'Smith', '2345678901', 'jane.smith@example.com', '2023-02-20', 'ACTIVE'),
('Alice', 'Brown', '3456789012', 'alice.brown@example.com', '2023-03-05', 'ACTIVE'),
('Bob', 'Johnson', '4567890123', 'bob.johnson@example.com', '2023-04-10', 'ACTIVE'),
('Charlie', 'Williams', '5678901234', 'charlie.williams@example.com', '2023-05-01', 'ACTIVE');

-- Insert Orders
INSERT INTO `Order` (customer_id, order_date, order_status, total_amount)
VALUES
(1, '2023-05-10 10:00:00', 'PENDING', 45.00),
(2, '2023-05-11 11:30:00', 'COMPLETED', 120.00),
(1, '2023-05-12 14:15:00', 'PENDING', 60.00),
(3, '2023-05-13 09:45:00', 'PENDING', 80.00),
(4, '2023-05-14 16:20:00', 'PENDING', 150.00);

-- Insert Payments
INSERT INTO Payment (order_id, payment_date, payment_method, amount)
VALUES
(2, '2023-05-11 12:00:00', 'CREDIT_CARD', 120.00),
(5, '2023-05-14 17:00:00', 'PAYPAL', 150.00);

-- Insert OrderItems
INSERT INTO OrderItem (order_id, product_type, product_id, quantity, price_each)
VALUES
(1, 'MOVIE', 1, 1, 15.00),
(1, 'ALBUM', 1, 1, 30.00),
(2, 'MOVIE', 2, 2, 20.00),
(3, 'MOVIE', 3, 1, 60.00),
(4, 'ALBUM', 2, 1, 80.00),
(5, 'MOVIE', 4, 1, 50.00),
(5, 'ALBUM', 3, 2, 50.00);

-- Insert Movies
INSERT INTO Movie (title, release_date, rating, genre, runtime_minutes, stock_count)
VALUES
('The Matrix', '1999-03-31', 'R', 'Sci-Fi', 136, 20),
('Drive', '2011-09-16', 'R', 'Action/Crime', 100, 15),
('Revenge of the Sith', '2005-05-19', 'PG-13', 'Sci-Fi/Action', 140, 25),
('The Big Lebowski', '1998-03-06', 'R', 'Comedy', 117, 30);

-- Insert Actors
INSERT INTO Actor (first_name, last_name, birth_date)
VALUES
('Keanu', 'Reeves', '1964-09-02'),
('Carrie-Anne', 'Moss', '1967-08-21'),
('Laurence', 'Fishburne', '1961-07-30'),
('Ryan', 'Gosling', '1980-11-12'),
('Carey', 'Mulligan', '1985-05-28'),
('Ewan', 'McGregor', '1971-03-31'),
('Hayden', 'Christensen', '1981-04-19'),
('Jeff', 'Bridges', '1949-12-04'),
('John', 'Goodman', '1952-06-20'),
('Julianne', 'Moore', '1960-12-03');

-- Insert Movie_Actor associations
-- For "The Matrix" (assumed movie_id = 1):
INSERT INTO Movie_Actor (movie_id, actor_id, role_name)
VALUES
(1, (SELECT actor_id FROM Actor WHERE first_name = 'Keanu' AND last_name = 'Reeves' LIMIT 1), 'Neo'),
(1, (SELECT actor_id FROM Actor WHERE first_name = 'Carrie-Anne' AND last_name = 'Moss' LIMIT 1), 'Trinity'),
(1, (SELECT actor_id FROM Actor WHERE first_name = 'Laurence' AND last_name = 'Fishburne' LIMIT 1), 'Morpheus');

-- For "Drive" (assumed movie_id = 2):
INSERT INTO Movie_Actor (movie_id, actor_id, role_name)
VALUES
(2, (SELECT actor_id FROM Actor WHERE first_name = 'Ryan' AND last_name = 'Gosling' LIMIT 1), 'Driver'),
(2, (SELECT actor_id FROM Actor WHERE first_name = 'Carey' AND last_name = 'Mulligan' LIMIT 1), 'Irene');

-- For "Revenge of the Sith" (assumed movie_id = 3):
INSERT INTO Movie_Actor (movie_id, actor_id, role_name)
VALUES
(3, (SELECT actor_id FROM Actor WHERE first_name = 'Ewan' AND last_name = 'McGregor' LIMIT 1), 'Obi-Wan Kenobi'),
(3, (SELECT actor_id FROM Actor WHERE first_name = 'Hayden' AND last_name = 'Christensen' LIMIT 1), 'Anakin Skywalker');

-- For "The Big Lebowski" (assumed movie_id = 4):
INSERT INTO Movie_Actor (movie_id, actor_id, role_name)
VALUES
(4, (SELECT actor_id FROM Actor WHERE first_name = 'Jeff' AND last_name = 'Bridges' LIMIT 1), 'The Dude'),
(4, (SELECT actor_id FROM Actor WHERE first_name = 'John' AND last_name = 'Goodman' LIMIT 1), 'Walter'),
(4, (SELECT actor_id FROM Actor WHERE first_name = 'Julianne' AND last_name = 'Moore' LIMIT 1), 'Maude');

-- Insert MusicAlbums
INSERT INTO MusicAlbum (title, release_date, genre, stock_count)
VALUES
('X&Y', '2005-06-06', 'Alternative/Pop', 25),
('Morning Glory', '1995-10-02', 'Rock/Alternative', 30),
('Discovery', '2001-03-12', 'Electronic', 20);

-- Insert Artists
INSERT INTO Artist (artist_name, start_year, end_year, active_status)
VALUES
('Coldplay', 1996, NULL, 'ACTIVE'),
('Oasis', 1991, 2009, 'INACTIVE'),
('Daft Punk', 1993, 2021, 'INACTIVE');

-- Insert Album_Artist associations
INSERT INTO Album_Artist (album_id, artist_id)
VALUES
(1, (SELECT artist_id FROM Artist WHERE artist_name = 'Coldplay' LIMIT 1)),
(2, (SELECT artist_id FROM Artist WHERE artist_name = 'Oasis' LIMIT 1)),
(3, (SELECT artist_id FROM Artist WHERE artist_name = 'Daft Punk' LIMIT 1));

