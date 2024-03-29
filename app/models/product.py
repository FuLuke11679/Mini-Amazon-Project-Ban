from flask import current_app as app
from flask import jsonify
#initializes product
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

    @classmethod
    def new_product(cls, name, price, amount, photo_url, seller_id, longDescription, tag, subtag):
        """
        Factory method for creating a new product instance without an id.
        """
        return cls(None, name, price, amount, True, photo_url, seller_id, longDescription, tag, subtag)

    #Returns product based on product_ID
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None
    
    #Returns products based on keyword
    @staticmethod
    def search(keyword):
        keyword = f"%{keyword}%"
        rows = app.db.execute('''
        SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
        FROM Products
        WHERE name LIKE :keyword OR longDescription LIKE :keyword
        ''', keyword=keyword)
        return [Product(*row) for row in rows]
    
    
    #Returns products based on tag
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
    
    #Returns products based on subtag
    @staticmethod
    def get_subtags_by_tag(tag):
        rows = app.db.execute('''
            SELECT DISTINCT subtag
            FROM Products
            WHERE tag = :tag
        ''', tag=tag)
        return [row[0] for row in rows]
    
    #Returns products based on sort_order
    @staticmethod
    def just_order(sort_order):
        order_clause = 'price DESC' if sort_order == 'desc' else 'price ASC'
        rows = app.db.execute('''
            SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
            FROM Products
            ORDER BY {}
        '''.format(order_clause))
        return [Product(*row) for row in rows]
    
    #Returns products based on keyword and tag
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

    #Returns products based on keyword and sort order
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

    #Returns products based on subtag and sort_order
    @staticmethod
    def get_by_subtag(subtag, sort_order):
        order_clause = 'price DESC' if sort_order == 'desc' else 'price ASC'
        query = '''
            SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
            FROM Products
            WHERE subtag = :subtag
            ORDER BY {}
        '''.format(order_clause)
        rows = app.db.execute(query, subtag=subtag)
        return [Product(*row) for row in rows]

    #Returns products based on keyword, tag, and sort_order
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
    
    #Returns products based on keyword, subtag (which implies tag), and sort_order
    @staticmethod
    def search_with_everything(keyword, subtag, sort_order):
        keyword = f"%{keyword}%"
        order_clause = 'price DESC' if sort_order == 'desc' else 'price ASC'
        query = '''
            SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
            FROM Products
            WHERE (name LIKE :keyword OR longDescription LIKE :keyword)
            AND subtag = :subtag
            ORDER BY {}
        '''.format(order_clause)
        rows = app.db.execute(query, keyword=keyword, subtag=subtag)
        return [Product(*row) for row in rows]

    #Returns ALL products that are available
    @staticmethod
    def get_all_sorted(available=True, sort_order='asc', page=1, per_page=9):
        offset = (page-1) * per_page
        order_clause = 'price DESC' if sort_order == 'desc' else 'price ASC'
        rows = app.db.execute('''
    SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
    FROM Products
    WHERE available = :available
    ORDER BY {}
    LIMIT :per_page OFFSET :offset
    '''.format(order_clause), available=available,per_page = per_page, offset = offset)
        return [Product(*row) for row in rows]
    
    #Returns all products based on product_id
    @staticmethod
    def get_list_by_ids(product_ids):
        rows = app.db.execute('''
            SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
            FROM Products
            WHERE id IN :product_ids
        ''',
        product_ids=tuple(product_ids))
        return [Product(*row) for row in rows]

    #Returns the price of a product based on ID
    @staticmethod
    def get_amount_num(id):
        rows = app.db.execute('''
            SELECT amount
            FROM Products
            WHERE id = :id
        ''', id=id)
        return rows[0][0] if rows else None

    #Returns all products with pagination
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
    
    #Returns amount from Products
    @staticmethod
    def get_amount(id):
        rows = app.db.execute('''
            SELECT amount
            FROM Products
            WHERE id = :id
        ''', id=id)
        return rows[0][0] if rows else None


    #Returns list of products based on name (product name) and seller_ID. Used to check for duplicate listings by the same seller.
    @staticmethod
    def get_by_name_and_seller(name, seller_id):
        """
        Retrieve a product by name and seller ID.

        Args:
            name (str): The name of the product.
            seller_id (int): The ID of the seller (user).

        Returns:
            Product object if found, None otherwise.
        """
        db = app.db
        result = db.execute(
            "SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag "
            "FROM Products "
            "WHERE name = :name AND seller_id = :seller_id",
            name=name, seller_id=seller_id
        )
        if result:
            return result
        else:
            return None














    #Returns products based on keyword, tag, subtag, and sort_order. CAN REMOVE?
    @staticmethod
    def search_products(keyword, tag, subtag, sort_order):
        keyword = f"%{keyword}%"
        order_clause = 'price DESC' if sort_order == 'desc' else 'price ASC'

        query = '''
            SELECT id, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag
            FROM Products
            WHERE (name LIKE :keyword OR longDescription LIKE :keyword)
        '''

        if tag:
            query += ' AND tag = :tag'
        if subtag:
            query += ' AND subtag = :subtag'

        query += f' ORDER BY {order_clause}'

        rows = app.db.execute(query, keyword=keyword, tag=tag, subtag=subtag)
        return [Product(*row) for row in rows]