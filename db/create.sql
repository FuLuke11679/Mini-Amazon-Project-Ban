-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    amount INT NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    photo_url VARCHAR(255), -- Adding a new column for the photo URL
    seller_id INT NOT NULL REFERENCES Users(id)
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);


CREATE TABLE Inventory (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    /*amt INT NOT NULL REFERENCES Products(amount),*/
    time_added timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Wishes (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_added timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Sellers (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT UNIQUE NOT NULL REFERENCES Users(id)
);

CREATE TABLE SellerReviews (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    seller_uid INT NOT NULL REFERENCES Users(id),
    review VARCHAR(1000) NOT NULL,
    rating INT NOT NULL,
    upvotes INT NOT NULL,
    time_posted timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Carts (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_added timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    quantity INT NOT NULL
);


CREATE TABLE Reviews (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    review VARCHAR(1000) NOT NULL,
    rating INT NOT NULL,
    upvotes INT NOT NULL,
    time_posted timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

ALTER TABLE Reviews
    ADD CONSTRAINT oneUPPair UNIQUE (uid, pid)

ALTER TABLE SellerReviews
    ADD CONSTRAINT oneUSellerPair UNIQUE (uid, seller_id)
    
