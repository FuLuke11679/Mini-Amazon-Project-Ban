from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status):
        self.id = id
        self.uid = uid
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

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
LIMIT 5
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]


    @staticmethod
    def get_all(uid, page=1, per_page=20):
        offset = (page-1) * per_page
        rows = app.db.execute('''
SELECT id, uid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status
FROM Purchases
WHERE uid = :uid
ORDER BY time_purchased DESC
LIMIT :per_page OFFSET :offset
''',
                              uid=uid,
                              per_page = per_page,
                              offset=offset)
        return [Purchase(*row) for row in rows]




    @staticmethod
    def create_purchase(uid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status):
        try: 
            rows = app.db.execute("""
INSERT INTO Purchases(uid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status)
VALUES(:uid, :seller_id, :pid, :name, :photo_url, :tag, :quantity, :price_per_unit, :total_price, :time_purchased, :fulfillment_status)
RETURNING id
""",
                                  uid = uid,
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
            id = rows[0][0]
            return Purchase.get(id)
        except Exception as e:
            return None
