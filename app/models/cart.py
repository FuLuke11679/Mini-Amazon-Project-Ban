from flask import current_app as app
from flask import jsonify   

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
    def get_all(uid):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added, quantity
FROM Carts
WHERE uid = :uid
ORDER BY time_added DESC
''',
                              uid=uid)
        return [CartItem(*row) for row in rows]

