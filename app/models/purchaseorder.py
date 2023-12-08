from flask import current_app as app


class PurchaseOrder:
    def __init__(self, id, uid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status, address):
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
        self.address = address

    @staticmethod
    def get_all_seller_id(uid, page=1, per_page=20):
        offset = (page-1) * per_page
        rows = app.db.execute('''
SELECT Purchases.id, uid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status, address
FROM Purchases LEFT JOIN Users
ON Purchases.uid = Users.id
WHERE seller_id = :uid
ORDER BY time_purchased DESC
LIMIT :per_page OFFSET :offset
''',
                              uid=uid,
                              per_page = per_page,
                              offset=offset)
        return [PurchaseOrder(*row) for row in rows]