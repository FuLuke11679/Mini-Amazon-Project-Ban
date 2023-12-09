from flask import current_app as app
from flask import jsonify   

#initialize cart item
class CartItem:
    def __init__(self, id, uid, pid, time_added, quantity):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_added = time_added
        self.quantity = quantity
#gets by cart id primary key
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added, quantity
FROM Carts
WHERE id = :id
''',
                              id=id)
        return CartItem(*(rows[0])) if rows else None
#adds new item to carts table and updates quantity instead of the item is already there
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


#gets all items in cart by user id
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
#displays certain number of items in cart
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
#returns all items in cart to where the quantity in carts is greater than the amount in products
    @staticmethod
    def return_invalid(user_id):
        rows = app.db.execute('''
            SELECT c.id, c.uid, c.pid, c.time_added, c.quantity
            FROM Carts as c
            JOIN Products as p ON c.pid = p.id
            WHERE c.uid = :user_id AND c.quantity > p.amount
        ''', user_id=user_id)

        return [CartItem(*row) for row in rows]

#deletes all items from a users cart
    @staticmethod
    def delete_all(user_id):
        try:
            rows = app.db.execute('''
DELETE FROM Carts
WHERE uid = :user_id
''', 
                                user_id=user_id)
            return True
        except Exception as e:
            # Handle the exception (log it, return False, etc.)
            return False