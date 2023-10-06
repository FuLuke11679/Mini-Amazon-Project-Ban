\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY Wishes FROM 'Wishes.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.wishes_id_seq',
                         (SELECT MAX(id)+1 FROM Wishes),
                         false);

\COPY Carts FROM 'Carts.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.carts_id_seq',
                         (SELECT MAX(id)+1 FROM Carts),
                         false);

\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);               

\COPY Inventory FROM 'Inventory.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.inventory_id_seq',
                         (SELECT MAX(id)+1 FROM Inventory),
                         false);  

\COPY Reviews FROM 'Reviews.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.reviews_id_seq',
                         (SELECT MAX(id)+1 FROM Reviews),
                         false);

\COPY SellerReviews FROM 'SellerReviews.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.sellerreviews_id_seq',
                         (SELECT MAX(id)+1 FROM Reviews),
                         false);


\COPY Sellers FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.sellers_id_seq',
                         (SELECT MAX(id)+1 FROM Reviews),
                         false);
