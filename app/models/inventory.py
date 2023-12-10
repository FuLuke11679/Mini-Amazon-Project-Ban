from flask import current_app as app


#initializes inventory item
class InventoryItem:
    def __init__(self, id, uid, pid, time_added, quantity):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_added = time_added
        self.quantity = quantity

#gets an inventory item given the product's id
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added, quantity
FROM Inventory
WHERE id = :id
''',
                              id=id)
        return InventoryItem(*(rows[0])) if rows else None

#gets the inventory of a seller given their user id
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

#returns 0 if the given uid is not a seller, 1 otherwise
    @staticmethod
    def get_seller(uid):
        num = app.db.execute('''
SELECT COUNT(1)
FROM Sellers
WHERE uid = :uid
''',
                              uid=uid)
        return (num[0])
    
#gets highest id in sellers
    @staticmethod
    def get_num():
        num = app.db.execute('''
SELECT COUNT(id)
FROM Sellers
''',
                            )
        return (num[0])
