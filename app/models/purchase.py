from flask import current_app as app

#initialize Purchase
class Purchase:
    def __init__(self, id, uid, oid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status):
        self.id = id
        self.uid = uid
        self.oid = oid
        self.seller_id = seller_id
        self.pid = pid
        self.name = name
        self.photo_url = photo_url
        self.tag = tag
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.total_price = total_price
        self.time_purchased = time_purchased
        self.fulfillment_status = fulfillment_status
#gets specific purchase by primary key
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None
#gets rows of purchases that are after a time input
    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, oid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
LIMIT 5
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

#gets all purchases by user id with pagination
    @staticmethod
    def get_all(uid, page=1, per_page=20):
        offset = (page-1) * per_page
        rows = app.db.execute('''
SELECT id, uid, oid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status
FROM Purchases
WHERE uid = :uid
ORDER BY time_purchased DESC
LIMIT :per_page OFFSET :offset
''',
                              uid=uid,
                              per_page = per_page,
                              offset=offset)
        return [Purchase(*row) for row in rows]
#gets all uid 
    @staticmethod
    def get_all_by_order(uid, oid):
        rows = app.db.execute('''
SELECT id, uid, oid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status
FROM Purchases
WHERE uid = :uid AND oid = :oid
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              oid=oid)
        return [Purchase(*row) for row in rows]

#gets the max oid in the purchases table. Utilized when creating new orders
    @staticmethod
    def get_max_oid():
        rows = app.db.execute('''
            SELECT MAX(oid)
            FROM Purchases
        ''')

        if rows is not None and rows[0] is not None:
            max_id = rows[0][0]
            return max_id
        else:
            return None

#creates a new row in purchases and updates quantity from products
    @staticmethod
    def create_purchase(uid, oid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status):
        try: 
            app.db.execute('''
            UPDATE Products
            SET amount = amount - :quantity
            WHERE id = :pid
        ''', quantity=quantity, pid=pid)
            
            rows = app.db.execute("""
INSERT INTO Purchases(uid, oid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status)
VALUES(:uid, :oid, :seller_id, :pid, :name, :photo_url, :tag, :quantity, :price_per_unit, :total_price, :time_purchased, :fulfillment_status)
RETURNING id
""",
                                  uid = uid,
                                  oid = oid,
                                  seller_id = seller_id,
                                  pid = pid, 
                                  name = name,
                                  photo_url = photo_url,
                                  tag = tag,
                                  quantity = quantity, 
                                  price_per_unit = price_per_unit,
                                  total_price = total_price,
                                  time_purchased = time_purchased,
                                  fulfillment_status = fulfillment_status)
            return Purchase.get(oid)
        except Exception as e:
            return None

#gets all purchases by a user by seller id
    @staticmethod
    def get_all_seller_id(uid, page=1, per_page=20):
        offset = (page-1) * per_page
        rows = app.db.execute('''
SELECT Purchases.id, uid, oid, seller_id, pid, name, address, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status
FROM Purchases LEFT JOIN Users
ON Purchases.uid = Users.id
WHERE seller_id = :uid
ORDER BY time_purchased DESC
LIMIT :per_page OFFSET :offset
''',
                              uid=uid,
                              per_page = per_page,
                              offset=offset)
        return [Purchase(*row) for row in rows]




#get_all function with multiple ways to manipulate what you are getting (selller id, item tag, start date, end date)
    def get_all_by_modifier(uid, seller_id=None, tag=None, start_date=None, end_date=None):
        
        seller_id = seller_id if seller_id else None
        tag = tag if tag else None
        start_date = start_date if start_date else None
        end_date = end_date if end_date else None
        
        rows = app.db.execute('''
SELECT id, uid, oid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status
FROM Purchases
WHERE uid = :uid
AND (:seller_id IS NULL OR seller_id = :seller_id)
AND (:tag IS NULL OR tag = :tag)
AND (:start_date IS NULL OR time_purchased >= :start_date)
AND (:end_date IS NULL OR time_purchased <= :end_date)
ORDER BY time_purchased DESC
''',
                              uid = uid,
                              seller_id=seller_id,
                              tag=tag,
                              start_date=start_date,
                              end_date=end_date)
        return [Purchase(*row) for row in rows]