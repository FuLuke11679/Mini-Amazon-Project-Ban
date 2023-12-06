from flask import current_app as app
from flask import jsonify   
#test

class CartItem:
    def __init__(self, id, uid, pid, time_added, quantity):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_added = time_added
        self.quantity = quantity

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added, quantity
FROM Carts
WHERE id = :id
''',
                              id=id)
        return CartItem(*(rows[0])) if rows else None
    @staticmethod
    def add(uid, pid, time_added, quantity):
        try:
            rows = app.db.execute("""
UPDATE Carts
SET quantity = quantity + :quantity
WHERE uid = :uid AND pid = :pid
""",
                                    uid=uid,
                                    pid=pid,
                                    time_added=time_added,
                                    quantity = quantity
                                    )
            if rows.rowcount > 0:
                return CartItem.get(id)
        except Exception as e: 
            rows = app.db.execute("""
INSERT INTO Carts(uid, pid, time_added, quantity)
VALUES(:uid, :pid, :time_added, :quantity)
RETURNING id
""",
                                uid=uid,
                                pid=pid,
                                time_added=time_added,
                                quantity = quantity
                                )
            id = rows[0][0]
            return CartItem.get(id)

    
    @staticmethod
    def get_all(uid, page=1, per_page=10):
        offset = (page-1) * per_page
        rows = app.db.execute('''
SELECT id, uid, pid, time_added, quantity
FROM Carts
WHERE uid = :uid
ORDER BY time_added DESC
LIMIT :per_page OFFSET :offset
''',
                              uid=uid,
                              per_page = per_page,
                              offset=offset)
        return [CartItem(*row) for row in rows]
    
    @staticmethod
    def display_num(uid, num_rows, offset):
        times = offset*num_rows
        rows = app.db.execute('''
SELECT id, uid, pid, time_added, quantity
FROM CARTS
WHERE uid = :uid
ORDER BY time_added DESC
LIMIT :num_rows OFFSET :times
''',
                              uid=uid,
                              num_rows = num_rows,
                              times = times)
        return [CartItem(*row) for row in rows]

