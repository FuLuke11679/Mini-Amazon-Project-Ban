from flask import current_app as app
from flask import jsonify


class Product:
    def __init__(self, id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag):
        self.id = id
        self.name = name
        self.price = price
        self.amount = amount
        self.available = available
        self.photo_url = photo_url
        self.seller_id = seller_id
        self.longDescription = longDescription
        self.tag = tag
        self.subtag = subtag

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None
    
    @staticmethod
    def get_all(available=True, page=1, per_page=10):
        offset = (page-1) * per_page
        rows = app.db.execute('''
SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
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
        SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
        FROM Products
        ORDER BY price DESC
        LIMIT :k
    ''', k=k)
        return [Product(*row) for row in rows]

    @staticmethod
    def search(keyword):
        keyword = f"%{keyword}%"
        rows = app.db.execute('''
        SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
        FROM Products
        WHERE name LIKE :keyword OR longDescription LIKE :keyword
        ''', keyword=keyword)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_by_tag(tag, sort_order):
        order_clause = 'price DESC' if sort_order == 'desc' else 'price ASC'
        rows = app.db.execute('''
        SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
        FROM Products
        WHERE tag = :tag ORDER BY {}
        '''.format(order_clause),
        tag=tag)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def search_in_category(keyword, tag):
        keyword = f"%{keyword}%"
        rows = app.db.execute('''
        SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
        FROM Products
        WHERE (name LIKE :keyword OR longDescription LIKE :keyword) AND tag = :tag
        ''',
        keyword=keyword, tag=tag)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_all_sorted(available=True, page=1, per_page=10, sort_order='asc'):
        offset = (page - 1) * per_page
        order_clause = 'price DESC' if sort_order == 'desc' else 'price ASC'
        rows = app.db.execute('''
SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
FROM Products
WHERE available = :available
ORDER BY {} 
LIMIT :per_page OFFSET :offset
'''.format(order_clause),
                              available=available, 
                              per_page=per_page, 
                              offset=offset)
        return [Product(*row) for row in rows]

    @staticmethod
    def search_sorted(keyword, sort_order='asc'):
        keyword = f"%{keyword}%"
        order_clause = 'price DESC' if sort_order == 'desc' else 'price ASC'
        rows = app.db.execute('''
SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
FROM Products
WHERE name LIKE :keyword OR longDescription LIKE :keyword
ORDER BY {}
'''.format(order_clause),
                              keyword=keyword)
        return [Product(*row) for row in rows]

    @staticmethod
    def search_in_category_sorted(keyword, tag, sort_order='asc'):
        keyword = f"%{keyword}%"
        order_clause = 'price DESC' if sort_order == 'desc' else 'price ASC'
        rows = app.db.execute('''
SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
FROM Products
WHERE (name LIKE :keyword OR longDescription LIKE :keyword) AND tag = :tag
ORDER BY {}
'''.format(order_clause),
                              keyword=keyword, tag=tag)
        return [Product(*row) for row in rows]



    @staticmethod
    def get_subtags_by_tag(tag):
        # Query the database to get subtags based on the selected category (tag)
        rows = app.db.execute('''
            SELECT DISTINCT subtag
            FROM Products
            WHERE tag = :tag
        ''', tag=tag)
        return [row[0] for row in rows]