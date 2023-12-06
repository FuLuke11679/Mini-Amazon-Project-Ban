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
        rows = app.db.execute('''SELECT quantity FROM Carts WHERE uid = :uid AND pid = :pid;''', uid=uid, pid=pid)

        if rows and len(rows) > 0:
            # Item already exists, update quantity
            app.db.execute("""
                UPDATE Carts
                SET quantity = quantity + :quantity
                WHERE uid = :uid AND pid = :pid
            """,
            uid=uid,
            pid=pid,
            time_added=time_added,
            quantity=quantity)

            # Return the CartItem corresponding to the updated item
            return CartItem.get(uid)
        else:
            # Item doesn't exist, insert new item
            rows = app.db.execute("""
                INSERT INTO Carts(uid, pid, time_added, quantity)
                VALUES(:uid, :pid, :time_added, :quantity)
                RETURNING id
            """,
            uid=uid,
            pid=pid,
            time_added=time_added,
            quantity=quantity)

            id = rows[0][0]
            # Return the CartItem corresponding to the new item
            return CartItem.get(uid)


    
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

