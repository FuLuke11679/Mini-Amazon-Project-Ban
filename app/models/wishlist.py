from flask import current_app as app  

#initializes wishlistitem
class WishlistItem:
    def __init__(self, id, uid, pid, time_added):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_added = time_added
#gets wishlist item by id primary key
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added
FROM Wishes
WHERE id = :id
''',
                              id=id)
        return WishlistItem(*(rows[0])) if rows else None
#gets all from wishlist table for a given user since a given time
#and orders by time adde descending
    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added
FROM Wishes
WHERE uid = :uid
AND time_added>= :since
ORDER BY time_added DESC
''',
                              uid=uid,
                              since=since)
        return [WishlistItem(*row) for row in rows]
#gets a specific wishlist item by primary key id
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added
FROM Wishes
WHERE id = :id
''',
                              id=id)
        return WishlistItem(*(rows[0])) if rows else None

#adds item to wishlist table
    @staticmethod
    def add(uid, pid, time_added):
        rows = app.db.execute("""
INSERT INTO Wishes(uid, pid, time_added)
VALUES(:uid, :pid, :time_added)
RETURNING id
""",
                                uid=uid,
                                pid=pid,
                                time_added=time_added)
        id = rows[0][0]
        return WishlistItem.get(id)

        

#gets all wishlist item for a given user by uid
    @staticmethod
    def get_all(uid):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added
FROM Wishes
WHERE uid = :uid
ORDER BY time_added DESC
''',
                              uid=uid)
        return [WishlistItem(*row) for row in rows]

