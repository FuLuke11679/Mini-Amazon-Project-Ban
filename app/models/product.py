from flask import current_app as app


class Product:
    def __init__(self, id, name, price, amount, available, photo_url, seller_id, longDescription, tag):
        self.id = id
        self.name = name
        self.price = price
        self.amount = amount
        self.available = available
        self.photo_url = photo_url
        self.seller_id = seller_id
        self.longDescription = longDescription
        self.tag = tag

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None
    
    @staticmethod
    def get_all(available=True, page=1, per_page=10):
        offset = (page-1) * per_page
        rows = app.db.execute('''
SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag
FROM Products
WHERE available = :available
LIMIT :per_page OFFSET :offset

''',
                              available=available, 
                              per_page = per_page, 
                              offset = offset)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_amount(id):
        rows = app.db.execute('''
SELECT amount
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None
    def get_top_k_expensive(k):
        rows = app.db.execute('''
        SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag
        FROM Products
        ORDER BY price DESC
        LIMIT :k
    ''', k=k)
        return [Product(*row) for row in rows]


    @staticmethod
    def get_list_by_ids(product_ids):
        # Use WHERE id IN (:product_ids) to filter by a list of product IDs
        rows = app.db.execute('''
            SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
            FROM Products
            WHERE id IN :product_ids
        ''',
        product_ids=tuple(product_ids))
        
        return [Product(*row) for row in rows]
