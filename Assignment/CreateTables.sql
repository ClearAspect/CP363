-- Create and select the database
CREATE DATABASE IF NOT EXISTS MovieMusicStore;
USE MovieMusicStore;

-- 1. CUSTOMER
CREATE TABLE Customer (
    customer_id 	INT AUTO_INCREMENT PRIMARY KEY,
    first_name 		VARCHAR(50) NOT NULL,
    last_name 		VARCHAR(50) NOT NULL,
    phone 			VARCHAR(15),
    email 			VARCHAR(100) NOT NULL UNIQUE,
    join_date 		DATE NOT NULL,
    status 			VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'

);

-- 2. ORDER
CREATE TABLE `Order` (
    order_id 		INT AUTO_INCREMENT PRIMARY KEY,
    customer_id 	INT NOT NULL,
    order_date 		DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    order_status 	VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    total_amount 	DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT fk_order_customer
        FOREIGN KEY (customer_id)
        REFERENCES Customer(customer_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 3. PAYMENT
CREATE TABLE Payment (
    payment_id 		INT AUTO_INCREMENT PRIMARY KEY,
    order_id 		INT NOT NULL,
    payment_date 	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_method 	VARCHAR(50) NOT NULL,
    amount 			DECIMAL(8,2) NOT NULL,
    CONSTRAINT fk_payment_order
        FOREIGN KEY (order_id)
        REFERENCES `Order`(order_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 4. ORDERITEM (Weak Entity)
CREATE TABLE OrderItem (
    order_item_id 	INT AUTO_INCREMENT PRIMARY KEY,
    order_id 		INT NOT NULL,
    product_type 	VARCHAR(10) NOT NULL,
    product_id 		INT NOT NULL,
    quantity 		INT NOT NULL DEFAULT 1,
    price_each 		DECIMAL(8,2) NOT NULL,
    CONSTRAINT fk_orderitem_order
        FOREIGN KEY (order_id)
        REFERENCES `Order`(order_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 5. MOVIE
CREATE TABLE Movie (
    movie_id 		INT AUTO_INCREMENT PRIMARY KEY,
    title 			VARCHAR(150) NOT NULL,
    release_date 	DATE,
    rating 			VARCHAR(10),
    genre 			VARCHAR(50),
    runtime_minutes INT NOT NULL,
    stock_count 	INT NOT NULL DEFAULT 0
); 

-- 6. ACTOR
CREATE TABLE Actor (
    actor_id 	INT AUTO_INCREMENT PRIMARY KEY,
    first_name 	VARCHAR(50) NOT NULL,
    last_name 	VARCHAR(50) NOT NULL,
    birth_date 	DATE
); 

-- 7. MOVIE_ACTOR (Associative Entity for Movie <-> Actor M:N)
CREATE TABLE Movie_Actor (
    movie_id 	INT NOT NULL,
    actor_id 	INT NOT NULL,
    role_name 	VARCHAR(100),
    PRIMARY KEY (movie_id, actor_id),
    CONSTRAINT fk_movieactor_movie
        FOREIGN KEY (movie_id)
        REFERENCES Movie(movie_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_movieactor_actor
        FOREIGN KEY (actor_id)
        REFERENCES Actor(actor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
); 

-- 8. MUSICALBUM
CREATE TABLE MusicAlbum (
    album_id 		INT AUTO_INCREMENT PRIMARY KEY,
    title 			VARCHAR(150) NOT NULL,
    release_date 	DATE,
    genre 			VARCHAR(50),
    stock_count 	INT NOT NULL DEFAULT 0
); 

-- 9. ARTIST
CREATE TABLE Artist (
    artist_id 		INT AUTO_INCREMENT PRIMARY KEY,
    artist_name 	VARCHAR(100) NOT NULL,
    start_year 		YEAR,
    end_year 		YEAR,
    active_status 	VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
); 

-- 10. ALBUM_ARTIST (Associative Entity for MusicAlbum <-> Artist M:N)
CREATE TABLE Album_Artist (
    album_id 	INT NOT NULL,
    artist_id 	INT NOT NULL,
    PRIMARY KEY (album_id, artist_id),
    CONSTRAINT fk_albumartist_album
        FOREIGN KEY (album_id)
        REFERENCES MusicAlbum(album_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_albumartist_artist
        FOREIGN KEY (artist_id)
        REFERENCES Artist(artist_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
); 

