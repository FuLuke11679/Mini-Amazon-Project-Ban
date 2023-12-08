from flask import current_app as app


class InventoryItem:
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
FROM Inventory
WHERE id = :id
''',
                              id=id)
        return InventoryItem(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added, quantity
FROM Inventory
WHERE uid = :uid
AND time_added >= :since
ORDER BY time_added DESC
''',
                              uid=uid,
                              since=since)
        return [InventoryItem(*row) for row in rows]
    
    @staticmethod
    def get_seller(uid):
        num = app.db.execute('''
SELECT COUNT(1)
FROM Sellers
WHERE uid = :uid
''',
                              uid=uid)
        return (num[0])

